from django.shortcuts import render, redirect
from django import forms
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry_page(request, title):
    entry = util.get_entry(title)
    entry_html = markdown2.markdown(entry)
    return render(request, "encyclopedia/layout.html", {
        "title": title,
        "content": entry_html
    })

    
#Form for creating article
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Content")
    
def create_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if util.save_entry(title, content):
                return redirect(f"/wiki/{title}")
            else:
                return render(request, "encyclopedia/create_page.html", {
                    "form": form,
                    "error": "A page with this title already exists."
                })
    else:
        form = NewEntryForm()
    
    return render(request, "encyclopedia/create_page.html", {
        "form": form
    })
    
def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry_page', title=random_entry)
    else:
        return render(request, "encyclopedia/error.html", {"message": "No entries found."})
    
def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, "encyclopedia/search.html", {"results": [], "query": query})
    
    entries = util.list_entries()
    
    if query.lower() in [entry.lower() for entry in entries]:
        return redirect('entry_page', title = query)
    
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

