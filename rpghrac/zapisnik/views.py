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
            return HttpResponseRedirect(reverse("zapisnik-edit", kwargs={"zapisek" : article.pk}))

    if not article_form:
        article_form = ArticleForm()

    return direct_to_template(request, template, {
        'article_form' : article_form,
    })


@commit_on_success
def edit(request, zapisek, template="zapisnik/edit.html"):
    article_form = None

    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)

    article = Article.objects.get(pk=zapisek)

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        
        if article_form.is_valid():
            article.description = article_form.cleaned_data['annotation']
            article.title = article_form.cleaned_data['title']
            article.tags = article_form.cleaned_data['tags']

            content = article.content
            content.content = article_form.cleaned_data['content']
            content.title = article.title

            article.save()
            content.save()

            return HttpResponseRedirect(reverse("zapisnik-edit", kwargs={"zapisek" : article.pk}))

    if not article_form:
        article_form = ArticleForm({
            "annotation" : article.description,
            "title" : article.title,
            "content" : article.content,
            "tags" : ', '.join([tag.name for tag in article.tags])
        })

    return direct_to_template(request, template, {
        'article_form' : article_form,
    })

def workshop(request, template="zapisnik/workshop.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    articles = zapisnik.get_drafts()

    return direct_to_template(request, template, {
        'articles' : articles
    })
