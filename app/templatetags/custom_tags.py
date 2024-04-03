from django import template

register = template.Library()

@register.filter
def star(value):  # Only one argument.
    string=""
    ye="❤️"
    ne="🖤"
    for i in range(5):
        if i>=value:
            string+=ne
        else:
            string+=ye
    return string

@register.filter
def custom_userauth(value):
    if value==9:
        return "Admin"
    return "Normal"