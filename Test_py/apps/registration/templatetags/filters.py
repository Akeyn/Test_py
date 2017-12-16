from django import template
from ..forms import *

register = template.Library()


@register.filter(name='show_results')
def show_results(arg):
    meter = Meter.objects.get(id=arg)
    type = TypeMeter.objects.get(id=meter.type_meter_id)
    return type.type_meter_name
