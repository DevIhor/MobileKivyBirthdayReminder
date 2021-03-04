import datetime


def calculate_age(born):
    today = datetime.datetime.now()
    years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    months = (12 + today.month - born.month - (today.day < born.day)) % 12
    return f"{years} years {months} months" if years and months else f"{years} years"