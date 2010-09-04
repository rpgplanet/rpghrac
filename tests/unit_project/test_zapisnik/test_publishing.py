# -*- coding: utf-8 -*-

"""
Check we're playing nicely with our version of django-markup
"""

from djangosanetesting import DatabaseTestCase
from djangosanetesting.utils import mock_settings

from ella.core.models import Category, Listing

from rpgcommon.user.user import create_user
from rpghrac.zapisnik.zapisnik import Zapisnik

class TestArticleManipulation(DatabaseTestCase):

    def prepare(self):
        self.user = create_user("tester", "xxx", "tester@example.com")
        self.zapisnik = Zapisnik(site=self.user.get_profile().site, owner=self.user, visitor=self.user)
        self.article = self.zapisnik.create_article_draft(
            annotation = "annotation",
            title = "title",
            content = """This is ""article"" content""",
            tags = "tagity tag"
        )

        # we're all about rpg, thou shall be there

    @mock_settings("DYNAMIC_RPGPLAYER_CATEGORIES", [
        {
            "tree_path" : "rpg",
            "parent_tree_path" : "",
            "title" : "RPG",
            "slug" : "rpg",
        },
    ])

    def test_article_appears_in_proper_listing(self):
        self.prepare()
        self.zapisnik.publish_article(article=self.article, categories=["rpg"])

        # if we take published articles now, we shall find ourselves there
        category = Category.objects.get(
            site = self.user.get_profile().site,
            tree_path = "rpg"
        )

        listings = Listing.objects.filter(
            category = category
        )

        self.assert_equals(1, len(listings))

        self.assert_equals(self.article.publishable_ptr, listings[0].target)

    @mock_settings("DYNAMIC_RPGPLAYER_CATEGORIES", [
        {
            "tree_path" : "rpg",
            "parent_tree_path" : "",
            "title" : "RPG",
            "slug" : "rpg",
        },
        {
            "tree_path" : "rpg/drd",
            "parent_tree_path" : "rpg",
            "title" : "Dračí Doupě",
            "slug" : "drd",
        },
    ])
    def test_article_can_be_republished(self):
        self.prepare()
        self.zapisnik.publish_article(article=self.article, categories=["rpg"])
        self.zapisnik.publish_article(article=self.article, categories=["drd"])

        # if we take published articles now, we shall find ourselves there
        rpg_cat = Category.objects.get(
            site = self.user.get_profile().site,
            tree_path = "rpg"
        )

        drd_cat = Category.objects.get(
            site = self.user.get_profile().site,
            tree_path = "rpg/drd"
        )

        listings = Listing.objects.filter(
            category = drd_cat
        )

        # we are in drd
        self.assert_equals(1, len(listings))
        self.assert_equals(self.article.publishable_ptr, listings[0].target)

        # but not in rpg anymore
        self.assert_equals(0, len(Listing.objects.filter(category=rpg_cat)))


    @mock_settings("DYNAMIC_RPGPLAYER_CATEGORIES", [
        {
            "tree_path" : "rpg",
            "parent_tree_path" : "",
            "title" : "RPG",
            "slug" : "rpg",
        },
        {
            "tree_path" : "rpg/drd",
            "parent_tree_path" : "rpg",
            "title" : "Dračí Doupě",
            "slug" : "drd",
        },
    ])
    def test_article_can_be_republished_in_same_category_too(self):
        self.prepare()
        self.zapisnik.publish_article(article=self.article, categories=["rpg"])
        self.zapisnik.publish_article(article=self.article, categories=["drd", "rpg"])

        # if we take published articles now, we shall find ourselves there
        rpg_cat = Category.objects.get(
            site = self.user.get_profile().site,
            tree_path = "rpg"
        )

        drd_cat = Category.objects.get(
            site = self.user.get_profile().site,
            tree_path = "rpg/drd"
        )

        # we are in drd
        self.assert_equals(1, len(Listing.objects.filter(category = drd_cat)))
        self.assert_equals(1, len(Listing.objects.filter(category=rpg_cat)))


    def test_draft_in_drafts(self):
        self.prepare()

        self.assert_equals(1, len(self.zapisnik.get_drafts()))

        self.assert_equals(self.article.content, self.zapisnik.get_drafts()[0].content)
        self.assert_equals(self.article.title, self.zapisnik.get_drafts()[0].title)


    @mock_settings("DYNAMIC_RPGPLAYER_CATEGORIES", [
        {
            "tree_path" : "rpg",
            "parent_tree_path" : "",
            "title" : "RPG",
            "slug" : "rpg",
        },
    ])
    def test_published_articles_not_in_draft(self):
        self.prepare()

        self.zapisnik.publish_article(article=self.article, categories=["rpg"])

        self.assert_equals(0, len(self.zapisnik.get_drafts()))
