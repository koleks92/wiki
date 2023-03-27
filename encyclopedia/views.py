from django.shortcuts import render
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        html = markdown2.markdown(util.get_entry(title))

        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
        })
    else:
        return render(request, "encyclopedia/notfound.html" , {
            "title": title.capitalize()
        })

