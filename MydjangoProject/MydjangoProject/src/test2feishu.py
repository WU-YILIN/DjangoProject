import os
import json
import pandas as pd
import requests


# 获取飞书 access_token，需要替换为你的 app_id 和 app_secret
def get_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            return result.get("tenant_access_token")
    return None


# 向飞书云文档表格写入数据
def write_to_feishu_table(access_token, spreadsheet_token, data):
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_update"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    requests_body = {
        "valueRanges": []
    }
    for table_name, df in data.items():
        values = [df.columns.tolist()] + df.values.tolist()
        value_range = {
            "range": f"{table_name}!A1",
            "values": values
        }
        requests_body["valueRanges"].append(value_range)

    response = requests.post(url, headers=headers, json=requests_body)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            print("数据已成功写入飞书云文档表格")
        else:
            print(f"写入飞书云文档表格失败，错误信息: {result.get('msg')}")
    else:
        print(f"请求飞书 API 失败，状态码: {response.status_code}")


def read_txt_files(folder_path):
    data = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                table_name = os.path.splitext(filename)[0]
                columns = []
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        json_data = json.load(file)
                        # 处理每个表的结构信息
                        for table_info in json_data.values():
                            current_table_name = table_info.get('table_name')
                            if not current_table_name:
                                continue
                            for column_name, column_info in table_info.get('columns', {}).items():
                                # 处理is_core字段（原示例中无对应数据，暂时留空）
                                is_core = ''
                                # 处理auto_increment字段
                                auto_increment = column_info.get('auto_increment', False)
                                columns.append([
                                    current_table_name,
                                    column_name,
                                    is_core,
                                    column_info.get('comment', ''),
                                    column_info.get('data_type', ''),
                                    column_info.get('raw_data_type', ''),
                                    'TRUE' if auto_increment else 'FALSE'
                                ])
                except FileNotFoundError:
                    print(f"文件 {file_path} 未找到。")
                except json.JSONDecodeError:
                    print(f"文件 {file_path} 不是有效的JSON格式。")
                except Exception as e:
                    print(f"读取文件 {file_path} 时发生错误: {e}")
                if columns:
                    df = pd.DataFrame(columns,
                                      columns=['table_name', 'columns_key', 'is_core', 'columns_comment',
                                               'columns_data_type', 'columns_raw_data_type', 'columns_auto_increment'])
                    data[table_name] = df
    except FileNotFoundError:
        print(f"文件夹 {folder_path} 未找到。")
    except Exception as e:
        print(f"处理文件夹 {folder_path} 时发生错误: {e}")
    return data


def save_to_excel(data, output_file):
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for table_name, df in data.items():
                df.to_excel(writer, sheet_name=table_name, index=False)
    except Exception as e:
        print(f"保存到 Excel 文件 {output_file} 时发生错误: {e}")


if __name__ == "__main__":
    folder_path = 'D:\\UM\\7014\\DjangoProject\\MydjangoProject\\MydjangoProject\\src\\folder'
    output_file = 'output.xlsx'
    app_id = 'cli_a77808f7b078500c'
    app_secret = 'I84eIfh3hQT0Sm2p203BqdETLKBTBhoE'
    spreadsheet_token = 'Wi4es23XVh1vyetsBtJc3c20nKf'

    data = read_txt_files(folder_path)
    if data:
        save_to_excel(data, output_file)
        print(f"数据已成功保存到 {output_file}")

        access_token = get_access_token(app_id, app_secret)
        if access_token:
            write_to_feishu_table(access_token, spreadsheet_token, data)
        else:
            print("获取飞书 access_token 失败")
    else:
        print("未找到有效数据。")
