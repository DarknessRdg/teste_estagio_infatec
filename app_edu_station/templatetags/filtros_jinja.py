from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(value, class_name, disabled=False):
    if disabled:
        return value.as_widget(attrs={'class': class_name, 'disabled': 'disabled'})
    else:
        return value.as_widget(attrs={'class': class_name})

@register.filter(name='float_com_ponto')
def float_com_ponto(value):
    return str(value).replace(',', '.')
