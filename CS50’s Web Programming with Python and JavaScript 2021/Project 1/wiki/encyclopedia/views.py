from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown2
from django import forms
from . import util


def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        form = request.POST
        if (util.get_entry(form.__getitem__('q')) == None and util.partial_search(form.__getitem__('q')) == None):
            return render(request, 'encyclopedia/not_found.html')
        elif (util.get_entry(form.__getitem__('q')) == None and util.partial_search(form.__getitem__('q')) != None):
            return render(request, 'encyclopedia/search_results.html', {
                "list": util.partial_search(form.__getitem__('q'))
            })
        else:
            page_rendered = markdown2.markdown_path("entries\\{}.md".format(form.__getitem__('q')))
            return render(request,'encyclopedia/page.html', {
                "page": page_rendered,
                "title": form.__getitem__('q')
            })


def page(request, title):
    if util.get_entry(title) == None:
        return render(request, 'encyclopedia/not_found.html')
    else:
        page_rendered = markdown2.markdown_path("entries\\{}.md".format(title))
        return render(request, 'encyclopedia/page.html', {
            "page": page_rendered,
            "title": title
        })


def random_page(request):
    return HttpResponseRedirect('wiki/{}'.format(str((util.random_result()))))

def edit_page(request,edition_entry):
    to_edit = (open("entries\\{}.md".format(edition_entry))).read()
    if request.method =="GET":
        return render(request, 'encyclopedia/edit.html', {
            "page": to_edit,
            "title": edition_entry
        })
    else:
        form = request.POST
        content = form.__getitem__('content')
        util.save_entry(edition_entry,content)
        return HttpResponseRedirect('/wiki/{}'.format(edition_entry))

class NewPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    def clean_title(self):
        title_passed = self.cleaned_data.get('title')
        existing_entries = util.list_entries()
        if title_passed in existing_entries:
            raise forms.ValidationError("The page with title '{}' already exists".format(title_passed))
        return title_passed

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPage
        })
    else:
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.new_page(title,content)
            return HttpResponseRedirect("/wiki/{}".format(title))
        else:
            return render(request, 'encyclopedia/new_page.html', {
                    "form": form
                })
