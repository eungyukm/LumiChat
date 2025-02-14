from django.shortcuts import render
from .models import LumiPrompt

def post(request):
    posts = LumiPrompt.objects.all() # Lumiprompt model DB
    title = [] # Lumiprompt title
    prompt=[]  # Lumiprompt prompt
    for post in posts:  # Loop through all the posts
        title.append(post.title) # Append the title
        prompt.append(post.prompt) # Append the prompt
    context = {
        'title': title,
        'prompt': prompt,
    } # title and prompt dictionary(context)
    return render(request, 'lumiprompt/main.html', context)