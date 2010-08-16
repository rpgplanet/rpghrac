# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from ella.core.models.main import Category, Author
from ella.core.models.publishable import Placement, PUBLISH_FROM_WHEN_EMPTY
from ella.articles.models import Article, ArticleContents

from tagging.models import Tag

TEXT_PROCESSOR = u'czechtile'
WORKING_CATEGORY = u'Dílna'

class Zapisnik(object):
    def __init__(self, owner, visitor=None, site=None):
        super(Zapisnik, self).__init__()

        self.owner = owner
        self.visitor = visitor
        self.site = site or self.owner.get_profile().site

    @property
    def root_category(self):
        try:
            return Category.objects.get(
                site = self.site,
                tree_parent = None
            )
        except Category.DoesNotExist:
            return Category.objects.create(
                site = self.site,
                tree_path = "",
                tree_parent = None,
                title = self.owner.username,
                slug = slugify(self.owner.username)
            )

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
