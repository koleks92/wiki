from django.shortcuts import render, redirect
from . import util
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


''' Helpers '''
# Help function to match entries(lowercase, uppercase, capitalize, snake etc.)
def name_check(name):
    entries = util.list_entries()
    for entry in entries:
        if (name.lower() == entry.lower()):
            return entry
    return False
        
# Check for substrings
def sub_check(str):
    entries = util.list_entries()
    results = []
    for entry in entries:
        if str.lower() in entry.lower():
            results.append(entry)
    
    return results

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Enyclopedia'}))

class NewForm(forms.Form):
    title = forms.CharField(label='',required=True, widget=forms.TextInput(attrs={'placeholder': 'New page title'}))
    content = forms.CharField(label='',required=True, widget=forms.Textarea(attrs={'placeholder': 'New page content'}))

class EditForm(forms.Form):
    content = forms.CharField(label='',required=True, widget=forms.Textarea(attrs={'placeholder': 'New page content'}))



''' Main functions '''
def index(request):

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm(),
        "entries": util.list_entries()
    })

def entry(request, title):
    if name_check(title):                           # Changing title to correct form
        title = name_check(title)
        html = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html" , {
            "form": SearchForm(),
            "title": title.capitalize(),
            "text": "Requested page was not found or was not added to our database yet."
        })
    
def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():                         # Check if valid and clean data
        search = form.cleaned_data['search']
        if name_check(search):                  # Check if any form of search is in entries
            search = name_check(search)
            return entry(request, search)
        elif sub_check(search):                 # Check if substring of any
            return render(request, 'encyclopedia/search.html', {
                "search": search,
                "results" : sub_check(search),
                "form": SearchForm()
            })
        else:                                   # Else render notfound page
            return render(request, "encyclopedia/notfound.html" , {
            "title": search.capitalize() + " - Not Found",
            "form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/layout.html", {
        "form": SearchForm(),
        "entries": util.list_entries()
        })
    
def random_page(request):
    return entry(request, random.choice(util.list_entries()))


def new_page(request):
    # TODO
    if request.method == "POST":
        content = NewForm(request.POST)
        if content.is_valid():                         # Check if valid and clean data
            title = content.cleaned_data['title']
            content = content.cleaned_data['content']
        if name_check(title):
            return render(request, "encyclopedia/error.html" , {
                "form": SearchForm(),
                "title": "Error",
                "text": "This title is already in our database."
            })
        else:
            util.save_entry(title, content)
            return entry(request, title)
            
        
    return render(request, "encyclopedia/new_page.html", {
        "new_form": NewForm(),
        "form": SearchForm()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    
    if request.method == "POST":
        content = EditForm(request.POST)
        if content.is_valid():                         # Check if valid and clean data
            content = content.cleaned_data['content']
            util.save_entry(title, content)
            return entry(request, title)


    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "edit_form": EditForm(initial={'content': content}),
        "form": SearchForm()
    })
    

