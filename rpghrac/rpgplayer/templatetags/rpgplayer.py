from django.template import Library, Node, Variable, TemplateSyntaxError

register = Library()

@register.tag
def player_last_articles(parser, token):
    """
    Template tag player_last_articles

    Usage:
        {% player_last_articles <user> as <variable> %}

        Return last 10 rpg player, non-draft article for given user


    Example:
        {% player_last_articles site_owner as articles %}
    """

    params = {}
    input = token.split_contents()

    o = 1

    params['user'] = input[o]
    o = o + 1

    # date
    if input[o] == 'as':
        params['variable'] = input[o+1]
    else:
        raise TemplateSyntaxError("'as' argument is expected on position %s" % o)
    print params
    return PlayerLastArticlesNode(params)

class PlayerLastArticlesNode(Node):
    def __init__(self, params):
        self.params = params

    def render(self, context):
        user = Variable(str(self.params['user'])).resolve(context)

        from rpghrac.zapisnik.zapisnik import Zapisnik

        zapisnik = Zapisnik(owner=user)

        context[self.params['variable']] = []

        return ''
