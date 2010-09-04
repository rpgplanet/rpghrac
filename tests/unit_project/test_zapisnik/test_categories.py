# -*- coding: utf-8 -*-

from djangosanetesting import DatabaseTestCase
from djangosanetesting.utils import mock_settings

from rpgcommon.user.user import create_user
from rpghrac.zapisnik.zapisnik import Zapisnik

class TestCategoryHandling(DatabaseTestCase):

    # cannot be in setUp because it depends on categories that are mocked on per-case bases
    def prepare(self):
        self.user = create_user("tester", "xxx", "tester@example.com")
        self.zapisnik = Zapisnik(site=self.user.get_profile().site, owner=self.user, visitor=self.user)
        self.article = self.zapisnik.create_article_draft(
            annotation = "annotation",
            title = "title",
            content = """This is ""article"" content""",
            tags = "tagity tag"
        )

    @mock_settings("DYNAMIC_RPGPLAYER_CATEGORIES", [
        {
            "tree_path" : "rpg",
            "parent_tree_path" : "",
            "title" : "RPG",
            "slug" : "rpg",
        },
    ])
    def test_tree_category_listing(self):
        self.prepare()
        root = self.zapisnik.get_available_categories_as_tree()

        self.assert_equals("", root['category'].tree_path)
        self.assert_equals(1, len(root['children']))
        self.assert_equals("RPG", root['children'][0]['category'].title)


