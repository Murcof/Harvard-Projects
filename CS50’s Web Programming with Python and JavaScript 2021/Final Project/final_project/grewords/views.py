from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Word,User
from django.http import JsonResponse
from django.core import serializers
from . import util
import random
from random import random, shuffle


# Create your views here.
def index(request):
    recent_words = Word.objects.all().order_by('-id')[:9]
    return render(request,"grewords/index.html",{
        "recent_words": recent_words,
        "alphabet": util.alphabet
    })

def word(request,word_id):
    word_info = Word.objects.get(pk=word_id)
    return render(request, "grewords/word.html", {
        "word": word_info,
        "alphabet": util.alphabet,
    })

def random(request):
    word_info = Word.objects.order_by('?')
    data = serializers.serialize('json', word_info[:1])
    return JsonResponse({"word": data}, status=200)

def search(request, word):
    #word_object = Word.objects.get(expression=(word.strip().lower()))
    try:
        word_object = Word.objects.get(expression=(word.strip().lower()))
        return HttpResponseRedirect(f"/{word_object.id}")
    except:
        return render(request, "grewords/search_results.html", {
            "results": util.partial_search(word.strip().lower()),
            "alphabet": util.alphabet
        })

def first_letter(request,letter):
    if letter == "All":
        results = Word.objects.all().order_by('-id')
        return render(request, "grewords/first_letter.html",{
            "results": results,
            "alphabet": util.alphabet
        })
    else:
        results = Word.objects.filter(expression__startswith=letter)
        return render(request, "grewords/first_letter.html", {
            "results": results,
            "alphabet": util.alphabet,
            "letter": letter
        })

def game(request,word_id):
    word_info = Word.objects.get(pk=word_id)
    random_words = Word.objects.order_by('?')[0:4]
    if word_info in random_words:
        pass
    else:
        random_words = random_words[0:3]
        random_words.append(word_info)
        shuffle(random_words)

    return render(request, "grewords/game.html", {
        "word": word_info,
        "alphabet": util.alphabet,
        "random_words": random_words
    })