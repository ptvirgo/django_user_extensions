from django import template

register = template.Library()

@register.inclusion_tag('registration/form_field.html') 
def ff(field):
    return {'field': field}
