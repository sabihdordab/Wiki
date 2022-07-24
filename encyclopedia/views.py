from django.shortcuts import render , reverse , HttpResponseRedirect
from django import forms
from markdown2 import Markdown
from django.contrib import messages
import random
from . import util


class Create_new_page(forms.Form):
    title =forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Page Title '}))
    content = forms.CharField(label = '', widget=forms.Textarea(attrs={
        'placeholder': 'Page Content using Markdown'
    }))


class Edit_page_content(forms.Form):
    content = forms.CharField(label = '', widget=forms.Textarea(attrs={
        'placeholder': 'Page Content using Markdown'
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
        title = request.GET.get('q', '')
        if title:
            if util.get_entry(title): #entry exists
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
            else:
                titles_list = util.similar_titles(title)
                return render(request, "encyclopedia/search.html", {
                "title": title,
                "titles_list": titles_list
                })
        #if not valid title :
        return render(request, 'encyclopedia/index.html' , {"entries": util.list_entries()})


def create(request):
    if request.method == "POST":
        form = Create_new_page(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title): #entry exists
                messages.add_message(
                request,
                messages.ERROR,
                message=f'{title} already exists !!',
                )
                return render(request, "encyclopedia/create.html", {"form": form})
            else:
                util.save_entry( title, content)
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
        else:
            return render(request, 'encyclopedia/create.html' , {'form' : form })
    # request.method is GET
    return render(request, 'encyclopedia/create.html' , {'form' : Create_new_page()})

def edit(request,title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content == None:
            return render(request,"encyclopedia/page_not_found.html", {
          "title": title
          })
        # content not None :
        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "form": Edit_page_content(initial={'content': content })})

    elif request.method == "POST" :
        form = Edit_page_content(request.POST)
        if form.is_valid():
              page_content = form.cleaned_data['content']
              util.save_entry(title, page_content)
              return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
        else:
              messages.add_message(
                    request,
                    messages.ERROR,
                    message=' You Have An Invalid Input!!',
                    )
              return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form })

def entry(request,title):
    Entry = util.get_entry(title)
    if Entry:
        EntryAsHTML = Markdown().convert(Entry)
        return render(request, "encyclopedia/entry.html",{
          "title": title,
          "content": EntryAsHTML
          })
    else :
        return render(request,"encyclopedia/page_not_found.html", {
          "title": title
          })

def randomEntry(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('encyclopedia:entry',args=[title]))
