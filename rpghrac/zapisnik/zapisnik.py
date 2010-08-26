# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from ella.core.models import (
    Category, Author,
    Listing, Placement, PUBLISH_FROM_WHEN_EMPTY
)
from ella.articles.models import Article, ArticleContents

from tagging.models import Tag

TEXT_PROCESSOR = u'czechtile'
WORKING_CATEGORY = u'Dílna'

def get_player_categories_as_choices():
    return [(i['slug'], i['title']) for i in settings.DYNAMIC_RPGPLAYER_CATEGORIES]


class Zapisnik(object):
    def __init__(self, owner, visitor=None, site=None):
        super(Zapisnik, self).__init__()

        self.owner = owner
        self.visitor = visitor
        self.site = site or self.owner.get_profile().site
        
        self._root_category = None

    @property
    def root_category(self):
        if not self._root_category:
            try:
                self._root_category = Category.objects.get(
                    site = self.site,
                    tree_parent = None
                )
            except Category.DoesNotExist:
                self._root_category = Category.objects.create(
                    site = self.site,
                    tree_path = "",
                    tree_parent = None,
                    title = self.owner.username,
                    #TODO: unixize
                    slug = slugify(self.owner.username)
                )
        return self._root_category

    @property
    def workshop_category(self):
        return Category.objects.get_or_create(
            site = self.site,
            tree_path = "dilna",
            tree_parent = self.root_category,
            title = WORKING_CATEGORY,
            slug = slugify(WORKING_CATEGORY)
        )[0]

    @property
    def site_author(self):
        return Author.objects.get_or_create(
            user = self.owner,
            name = self.owner.username,
            slug = slugify(self.owner.username)
        )[0]

    def get_drafts(self):
        return Article.objects.filter(
            authors = self.site_author,
            category = self.workshop_category
        )

    def get_article(self, pk):
        return Article.objects.get(
            pk = pk,
            authors = self.site_author,
            category = self.workshop_category
        )

    def get_published_articles(self):
        return Article.objects.filter(
            authors = self.site_author,
            publish_from__lte = datetime.now()
        )

    def create_article_draft(self, annotation, title, content, tags):
        category = self.workshop_category

        article = Article.objects.create(
            # updated = datetime.now()
            title = title,
            slug = slugify(title),
            content_type = ContentType.objects.get_for_model(Article),
            category = category
        )
        article.djangomarkup_description = annotation
        article.authors.add(self.site_author)

        article.save()

        acontent = ArticleContents(
            article = article,
            title = title
        )
        acontent.djangomarkup_content = content
        acontent.save()

        Tag.objects.update_tags(article, tags)

        Placement.objects.create(
            publishable = article.publishable_ptr,
            category = category,
            slug = article.slug,
            publish_from = PUBLISH_FROM_WHEN_EMPTY
        )

        return article

    def _get_parent_category_path(self, tree_path):
        return '/'.join([i for i in tree_path.split('/')][:-1])

    def _get_parent_category(self, tree_path):
        path = self._get_parent_category_path(tree_path)
        if path == self.root_category.tree_path:
            return self.root_category
        else:
            try:
                return Category.objects.get(
                    site = self.site,
                    tree_path = path
                )
            except Category.DoesNotExist:
                category_dict = [i for i in settings.DYNAMIC_RPGPLAYER_CATEGORIES if i['tree_path'] == path]
                if len(category_dict) < 1:
                    raise ImproperlyConfigured("DYNAMIC_RPGPLAYER_CATEGORIES contains category whose parent is not there!")

                category_dict = category_dict[0]

                return Category.objects.create(
                    site = self.site,
                    tree_path = category_dict['tree_path'],
                    tree_parent = self._get_parent_category(category_dict['tree_path']),
                    title = category_dict['title'],
                    slug = category_dict['slug']
                )

    def publish_article(self, article, categories):

        # We shall be more smart about this and only delete unpublished and update
        # those republished. After someone profiles this or has spare time
        Placement.objects.filter(publishable = article.publishable_ptr, category__site = self.site).delete()

        for category in categories:
            category_dict = [i for i in settings.DYNAMIC_RPGPLAYER_CATEGORIES if i['slug'] == category][0]

            placement = Placement.objects.create(
                publishable = article.publishable_ptr,
                slug = article.slug,
                publish_from = datetime.now(),
                category = Category.objects.get_or_create(
                    site = self.site,
                    tree_path = category_dict['tree_path'],
                    tree_parent = self._get_parent_category(category_dict['tree_path']),
                    title = category_dict['title'],
                    slug = category_dict['slug']
                )[0]
            )

            Listing.objects.create(
                placement = placement,
                category = placement.category,
                publish_from = placement.publish_from,
            )
