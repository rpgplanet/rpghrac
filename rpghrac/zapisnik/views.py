from django.http import Http404
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from ella.core.models.main import Category, Author, Source
from ella.articles.models import Article, ArticleContents

from rpghrac.zapisnik.forms import ArticleForm, PublishForm
from rpghrac.zapisnik.zapisnik import Zapisnik

def home(request, template="zapisnik/home.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    articles = zapisnik.get_published_articles()
    return direct_to_template(request, template, {
        'articles' : articles
    })

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
            article.djangomarkup_description = article_form.cleaned_data['annotation']
            article.title = article_form.cleaned_data['title']
            article.tags = article_form.cleaned_data['tags']

            article.content.djangomarkup_content = article_form.cleaned_data['content']
            article.content.title = article.title

            article.content.save()
            article.save()

            return HttpResponseRedirect(reverse("zapisnik-edit", kwargs={"zapisek" : article.pk}))

    if not article_form:
        article_form = ArticleForm({
            "annotation" : article.djangomarkup_description,
            "title" : article.title,
            "content" : article.content.djangomarkup_content,
            "tags" : ', '.join([tag.name for tag in article.tags])
        })

    return direct_to_template(request, template, {
        'article_form' : article_form,
        'article' : article
    })

def workshop(request, template="zapisnik/workshop.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    articles = zapisnik.get_drafts()

    return direct_to_template(request, template, {
        'articles' : articles
    })

def preview(request, zapisek_id, template="zapisnik/preview.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    try:
        article = zapisnik.get_article(pk=zapisek_id)
    except Article.DoesNotExists:
        raise Http404

    return direct_to_template(request, template, {
        'article' : article
    })

def publish(request, zapisek_id, template="zapisnik/publish.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    try:
        article = zapisnik.get_article(pk=zapisek_id)
    except Article.DoesNotExists:
        raise Http404

    publish_form = None

    if request.method == "POST":
        publish_form = PublishForm(request.POST, categories_tree = zapisnik.get_available_categories_as_tree())
        if publish_form.is_valid():
            zapisnik.publish_article(article=article, categories=publish_form.cleaned_data['categories'])

            #FIXME: Should lead to published article, to absolute url?
            return HttpResponseRedirect(reverse("zapisnik-home"))

    if not publish_form:
        publish_form = PublishForm(categories_tree = zapisnik.get_available_categories_as_tree())

    return direct_to_template(request, template, {
        'article' : article,
        'publish_form' : publish_form,
    })

# only list categories
def categories(request, template="zapisnik/categories.html"):
    zapisnik = Zapisnik(site=request.site, owner=request.site_owner, visitor=request.user)
    categories = zapisnik.get_available_categories_as_tree()
    return direct_to_template(request, template, {
        'categories' : categories,
    })
