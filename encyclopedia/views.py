from django.shortcuts import render, redirect
from . import util
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


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

class SearchWiki(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Enyclopedia'}))



''' Main functions '''
def index(request):

    return render(request, "encyclopedia/index.html", {
        "form": SearchWiki(),
        "entries": util.list_entries()
    })

def entry(request, title):
    if name_check(title):                           # Changing title to correct form
        title = name_check(title)
        html = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
        })
    else:
        return render(request, "encyclopedia/notfound.html" , {
            "title": title.capitalize()
        })
    
def search(request):
    form = SearchWiki(request.GET)
    if form.is_valid():                         # Check if valid and clean data
        search = form.cleaned_data['search']
        if name_check(search):                  # Check if any form of search is in entries
            search = name_check(search)
            print(search)
            return entry(request, search)
        elif sub_check(search):                 # Check if substring of any
            return render(request, 'encyclopedia/search.html', {
                "search": search,
                "results" : sub_check(search)
            })
        else:                                   # Else render notfound page
            return render(request, "encyclopedia/notfound.html" , {
            "title": search.capitalize()
            })
    else:
        return render(request, "encyclopedia/layout.html", {
        "form": SearchWiki(),
        "entries": util.list_entries()
        })
    
def random(request):
    # TODO

    

