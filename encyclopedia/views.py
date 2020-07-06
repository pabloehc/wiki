from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)

    if not content:
        content = f"Sorry! The page for {title} was not found!"
        title = "Error"
        

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

