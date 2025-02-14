from django.shortcuts import render
from .models import LumiPrompt

def post(request):
    posts = LumiPrompt.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'lumiprompt/main.html',context)