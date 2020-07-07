from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class PageForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Page\'s title'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Write the entry\'s content'}))

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
        "content": markdown2.markdown(content),
        "form": SearchForm()
    })

def new_page(request):
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']

            # check if an entry already existed
            previous = util.get_entry(title)

            if previous:
                return render(request, "encyclopedia/entry.html", {
                    "title": "Error",
                    "content": f"An entry for {title} already exists!"
                })
            
            else:
                util.save_entry(title, form.cleaned_data['content'])
                return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))
    
    # Get request
    else:
        return render (request, "encyclopedia/new_page.html", {
            "form": SearchForm(),
            'PageForm': PageForm()
        })

def edit_page(request, title):
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            util.save_entry(title, form.cleaned_data['content'])
            return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))

    else:
        pageform = PageForm({"title": title, "content": util.get_entry(title)})

        return render (request, "encyclopedia/edit_page.html", {
                "title": title,
                "form": SearchForm(),
                'PageForm': pageform
        })