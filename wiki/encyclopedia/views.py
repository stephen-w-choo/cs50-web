from django import forms
from django.shortcuts import render, redirect
from markdown2 import markdown
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from django.urls import reverse, resolve
import re
from random import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, entry):
    article = util.get_entry(entry)
    if article == None:
        return render(request, "encyclopedia/error.html", {
            "error": "Page does not exist"
        })
    article = markdown(article)

    return render(request, "encyclopedia/entry.html", {
        "article": article,
        "entry": entry
    })

def search(request):
    list = util.list_entries()
    search_query = request.GET.get("q")
    matches = []
    for entry in list:
        if search_query.lower() == entry.lower():
            return redirect("wiki:url_entry", entry=search_query)
        if re.search(search_query.lower(), entry.lower()):
            matches.append(entry)
    return render(request, "encyclopedia/search.html", {
        "matches": matches,
        "search_query": search_query
    })


def editpage(request, page_id=None):
    class PageForm(forms.Form):
        title = forms.CharField(label="title", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 800px; margin-bottom: 20px;', 'class': 'form-control'}))
        article = forms.CharField(label="article", widget=forms.Textarea(attrs={'style': 'width: 800px; margin-bottom: 20px;', 'class': 'form-control'}))

    if request.method == "GET":
        if page_id == None:
            return render(request, "encyclopedia/newpage.html", {
                "form": PageForm(),
            })

        else:
            page_content = util.get_entry(page_id)
            return render(request, "encyclopedia/editpage.html", {
                "form":PageForm(initial={"title": page_id, "article": page_content}),
                "pagename": page_id
            })

    if request.method == "POST":
        page = PageForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data["title"]
            article = page.cleaned_data["article"]
            original_title = page.data["original_title"]

            # for a new page, check if the title matches an existing page
            if original_title == "newpage":
                # then check if the title of the new page matches an existing page - if it does, return an error
                if title in util.list_entries():
                    return render(request, "encyclopedia/newpage.html", {
                        "form":PageForm(initial={"title": title, "article": article}),
                        "error": "Title of page already exists, please change the title"
                    })

            #For an existing page - check if the title has been changed
            if original_title != title:
                util.delete_entry(original_title)
                
            
            util.save_entry(title, article)
            
        return redirect("wiki:url_entry", entry = title)

def randompage(request):
    list = util.list_entries()
    randomarticle = list[int(random()*len(list))]
    return redirect("wiki:url_entry", entry = randomarticle)