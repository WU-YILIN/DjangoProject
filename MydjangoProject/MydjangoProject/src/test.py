import os
import json
import pandas as pd

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
    data = read_txt_files(folder_path)
    if data:
        save_to_excel(data, output_file)
        print(f"数据已成功保存到 {output_file}")
    else:
        print("未找到有效数据。")

