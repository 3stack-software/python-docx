import django.template 
register = django.template.Library() 
@register.filter 
def customfilter(stuff): 
    return "%s!" % stuff 
@register.filter
def cat(stuff): 
    return "MEOW %s" % stuff 
django.template.builtins.append(register)