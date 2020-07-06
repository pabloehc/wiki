from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):
    entries = util.list_entries()
    heading = "All Pages"

    if request.method == "POST":
        form = SearchForm(request.POST)
        
        if form.is_valid():
            query = form.cleaned_data["query"]
            # If entry exists, redirect to entry page
            if util.get_entry(query):
                return HttpResponseRedirect(reverse('entry', kwargs={'title': query}))
            
            # If it does not, check for "similar" entries
            else:
                tempEntries = []
                for entry in entries:
                    if query.lower() in entry.lower():
                        tempEntries.append(entry)
                entries = tempEntries
                heading = "Similar Pages"
                     
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form": SearchForm(),
        "heading": heading
    })

def entry(request, title):
    content = util.get_entry(title)

    if not content:
        content = f"Sorry! The page for {title} was not found!"
        title = "Error"
        

    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "content": content,
        "form": SearchForm()
    })