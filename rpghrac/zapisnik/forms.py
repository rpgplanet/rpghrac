# -*- coding: utf-8 -*-

from django.forms import (
    Form, ModelForm, BaseForm,
    Field,
    CharField, URLField, MultipleChoiceField, Textarea,
    IntegerField, RadioSelect, BooleanField, CheckboxSelectMultiple,
    ValidationError
)

from zapisnik import get_player_categories_as_choices


class ArticleForm(Form):
    title = CharField(label=u"Název")
    annotation = CharField(widget=Textarea(), label=u"Anotace")
    content = CharField(widget=Textarea(), label=u"Obsah")
    tags = CharField(label=u"Nálepky (oddělené mezerami nebo čárkami)", max_length=255)

class PublishForm(Form):
    categories = MultipleChoiceField(label=u"Kategorie", choices=get_player_categories_as_choices(), widget=CheckboxSelectMultiple())
