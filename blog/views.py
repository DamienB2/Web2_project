from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

posts = [
    {
        'author': 'Dam',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'November 9, 2023'
    },
    {
        'author': 'Bam',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'November 10, 2023'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
