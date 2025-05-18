from django.views.generic import ListView
from django.shortcuts import render
from .models import Review


class GameReviewListView(ListView):
    model = Review
    template_name = 'gamereview_list.html'
    context_object_name = 'reviews'

def review_list(request):
    reviews = Review.objects.all()  # 查询 Review 数据表里的所有记录
    return render(request, 'gamereview_list.html', {'reviews': reviews})
