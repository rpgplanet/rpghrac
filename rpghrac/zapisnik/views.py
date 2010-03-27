from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from ella.core.models.main import Category, Author, Source
from ella.articles.models import Article, ArticleContents

from rpghrac.zapisnik.forms import ArticleForm
from rpghrac.zapisnik.zapisnik import Zapisnik

def home(request, template="zapisnik/home.html"):
    return direct_to_template(request, template, {})

@commit_on_success
def new(request, template="zapisnik/new.html"):
    article_form = None

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():

            zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
            article = zapisnik.create_article_draft(
                annotation = article_form.cleaned_data['annotation'],
                title = article_form.cleaned_data['title'],
                content = article_form.cleaned_data['content'],
                tags = article_form.cleaned_data['tags']
            )

            #TODO: redirect to article
            return HttpResponseRedirect(reverse("zapisnik-home"))

    if not article_form:
        article_form = ArticleForm()

    return direct_to_template(request, template, {
        'article_form' : article_form,
    })

def workshop(request, template="zapisnik/workshop.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    articles = zapisnik.get_drafts()

    return direct_to_template(request, template, {
        'articles' : articles
    })
