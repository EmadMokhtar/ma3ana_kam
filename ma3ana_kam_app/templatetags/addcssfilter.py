from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(field, args):
    return field.as_widget(attrs={'class': args})