import datetime as dt


def validate_year(year):
    now_year = dt.date.today()

    if not 0 < year <= now_year.year:
        raise ValueError('Некорректный год!')
