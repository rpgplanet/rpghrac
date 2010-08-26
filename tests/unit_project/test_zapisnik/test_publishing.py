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

    def setUp(self):
        super(TestArticleManipulation, self).setUp()

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
    def test_article_published_by_update(self):
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

        

