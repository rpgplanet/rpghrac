# -*- coding: utf-8 -*-

"""
Check we're playing nicely with our version of django-markup
"""

from djangosanetesting import DatabaseTestCase
from ella.articles.models import Article

from rpgcommon.user.user import create_user
from rpghrac.zapisnik.zapisnik import Zapisnik



class TestArticleManipulation(DatabaseTestCase):

    def setUp(self):
        super(TestArticleManipulation, self).setUp()

        self.user = create_user("tester", "xxx", "tester@example.com")
        self.zapisnik = Zapisnik(site=self.user.get_profile().site, owner=self.user, visitor=self.user)

    def test_markup_rendered_properly_from_article(self):

        article = self.zapisnik.create_article_draft(
            annotation = "annotation",
            title = "title",
            content = """This is ""article"" content""",
            tags = "tagity tag"
        )

        self.assert_equals("<p>This is <em>article</em> content</p>", article.content.content.strip())

    def test_update_propagated(self):

        article = self.zapisnik.create_article_draft(
            annotation = "annotation",
            title = "title",
            content = """This is ""article"" content""",
            tags = "tagity tag"
        )

        update = Article.objects.get(pk=article.pk)
        update.content.djangomarkup_content = "Another content, *really*"

        update.title = "another title"
        update.content.title = update.title
        
        update.content.save()
        update.save()

        article = Article.objects.get(pk=update.pk)

        self.assert_equals("<p>Another content, <strong>really</strong></p>", article.content.content.strip())


