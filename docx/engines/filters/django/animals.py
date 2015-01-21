import django.template 
register = django.template.Library() 
@register.filter 
def cow(stuff): 
    return "MOOH %s" % stuff 
@register.filter
def dog(stuff): 
    return "WOOOF %s" % stuff 
django.template.builtins.append(register)