from datetime import datetime, timedelta
from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def custom_naturaltime(value):
    if not value:
        return ""

    if isinstance(value, str):
        if "dias atrás" in value:
            days_ago = int(value.split()[0])
            value = now() - timedelta(days=days_ago)
        else:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    if value > now():
        return "no futuro"

    diff = now() - value
    days = diff.days
    seconds = diff.seconds

    if days == 0:
        if seconds < 60:
            return f"Há {seconds} segundos atrás"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"Há {minutes} minutos atrás"
        else:
            hours = seconds // 3600
            return f"Há {hours} horas atrás"
    elif days == 1:
        return "Há 1 dia atrás"
    elif 1 < days < 7:
        return f"Há {days} dias atrás"
    elif days == 7:
        return "Há 1 semana atrás"
    elif 7 < days < 30:
        weeks = days // 7
        return f"Há {weeks} semanas atrás"
    elif days == 30:
        return "Há 1 mês atrás"
    elif 30 < days < 365:
        months = days // 30
        return f"Há {months} meses atrás"
    else:
        return value.strftime("%d/%m/%Y")


@register.filter
def get_qty_applications_per_user(dictionary, key):
    return dictionary.get(key)
