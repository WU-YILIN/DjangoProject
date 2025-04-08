from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from phoneReview.models import Brand, Model, Review


def index(request):
    reviews = Review.objects.all()
    return render(request, 'index.html', {'reviews': reviews})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_phone(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        origin = request.POST.get('origin')
        manufacturing_since = request.POST.get('manufacturing_since')
        model_name = request.POST.get('model_name')
        launch_date = request.POST.get('launch_date')
        platform = request.POST.get('platform')

        brand, created = Brand.objects.get_or_create(name=brand_name, origin=origin,
                                                     manufacturing_since=manufacturing_since)
        Model.objects.create(brand=brand, model_name=model_name, launch_date=launch_date, platform=platform)
        return redirect('index')
    return render(request, 'add_phone.html')


@login_required
def add_review(request):
    if request.method == 'POST':
        model_id = request.POST.get('model')
        review_article = request.POST.get('review_article')
        date_published = request.POST.get('date_published')

        related_model = Model.objects.get(id=model_id)
        review = Review.objects.create(review_article=review_article, date_published=date_published)
        review.related_models.add(related_model)
        return redirect('index')
    models = Model.objects.all()
    return render(request, 'add_review.html', {'models': models})


def model_reviews(request, model_name):  # 确保接受 model_name 参数
    # 如果 model_name 是空或无效，可以抛出自定义 404 错误
    if not model_name:
        raise Http404("Model name is missing.")

    # 根据手机型号筛选评论
    reviews = Review.objects.filter(related_models__model_name=model_name)
    if not reviews.exists():
        raise Http404(f"No reviews found for the model: {model_name}")

    # 渲染页面并传递评论数据
    return render(request, 'model_reviews.html', {'reviews': reviews, 'model_name': model_name})


from django.contrib.auth.decorators import login_required


@login_required  # 确保只有已登录用户才能访问
def profile(request):
    user = request.user  # 获取当前登录用户
    return render(request, 'profile.html', {'user': user})  # 将用户信息传递给模板

