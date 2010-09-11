# -*- coding: utf-8 -*-

from django.forms import (
    Form, ModelForm, BaseForm,
    Field,
    CharField, URLField, MultipleChoiceField, Textarea, ModelChoiceField,
    IntegerField, RadioSelect, BooleanField, CheckboxSelectMultiple, CheckboxInput,
    ValidationError
)

from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

class ArticleForm(Form):
    title = CharField(label=u"Název")
    annotation = CharField(widget=Textarea(), label=u"Anotace")
    content = CharField(widget=Textarea(), label=u"Obsah")
    tags = CharField(label=u"Nálepky (oddělené mezerami nebo čárkami)", max_length=255)


######### taken from django-mptt
from django.utils.encoding import smart_unicode
from django.forms.forms import BoundField
from itertools import chain

class TreeNodeMultipleCheckbox(CheckboxSelectMultiple):
    """A ModelChoiceField for tree nodes."""
    def __init__(self, categories_tree, *args, **kwargs):
        self.categories_tree = categories_tree

        super(TreeNodeMultipleCheckbox, self).__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        no = 0
        previous_node_depth = 0
        
        walk_list = getattr(self, "walk_list", [])
        
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            if walk_list and len(walk_list) > no:
                # special case is special
                if walk_list[no].tree_path == "":
                    node_depth = 0
                else:
                    node_depth = len(walk_list[no].tree_path.split("/"))
            else:
                node_depth = 0

            if node_depth < previous_node_depth:
                output.append((u'</ul>'*(previous_node_depth-node_depth)))

            if node_depth > previous_node_depth:
                output.append(u'<ul>')

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))

            previous_node_depth = node_depth
            no += 1
        
        # It's tree baby! There is no root at the end
        if 0 < previous_node_depth:
            output.append((u'</ul>'*(previous_node_depth)))

        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


class TreeMultipleChoiceField(MultipleChoiceField):
    def __init__(self, categories_tree, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):

        if not choices:
            choices, walk_list = self._get_choices_and_walk_list_from_tree(categories_tree)

        if widget:
            self.widget.walk_list = walk_list

        super(TreeMultipleChoiceField, self).__init__(choices=choices, required=required, \
                widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)

    def _append_node(self, node, choices, walk_list):
        #FIXME: This will cause collisions between tree/my-page and tree-my/page
        choices.append((slugify(node['category'].tree_path), node['category'].title))
        walk_list.append(node['category'])

        for child in node['children']:
            self._append_node(child, choices, walk_list)

    def _get_choices_and_walk_list_from_tree(self, categories_tree):
        choices = []
        walk_list = []

        # exception for root
        choices.append(('__root__', categories_tree['category'].title + u' (zobrazení na úvodní straně)'))
        walk_list.append(categories_tree['category'])

        for child in categories_tree['children']:
            self._append_node(child, choices, walk_list)

        return tuple(choices), walk_list


from django.forms.forms import BoundField

class PublishForm(Form):

    def __init__(self, categories_tree, *args, **kwargs):

        self.base_fields['categories'] = TreeMultipleChoiceField(
            label=u"Kategorie",
            categories_tree = categories_tree,
            widget = TreeNodeMultipleCheckbox(categories_tree = categories_tree)
        )

        super(PublishForm, self).__init__(*args, **kwargs)

    def as_ul(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._ul_html_output(u'<li>%(errors)s%(label)s %(field)s%(help_text)s</li>', u'<li>%s</li>', '</li>', u' %s', False)


    def _ul_html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        ##########
        ### Main hack goes like this: we want children to be rendered as <ul> *inside* parent <li>
        ### Thus, we render special tree items not as usual, but using helper atribute that sorted it as tree for us
        ##########

        for name, field in self.fields.items():
            bf = BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))
                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''
                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                output.append(normal_row % {'errors': force_unicode(bf_errors), 'label': force_unicode(label), 'field': unicode(bf), 'help_text': help_text})
        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = normal_row % {'errors': '', 'label': '', 'field': '', 'help_text': ''}
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))

