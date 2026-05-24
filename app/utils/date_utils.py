from datetime import date, datetime
from zoneinfo import ZoneInfo
import jdatetime


def gregorian_date_to_jalali_string(value):
    if not value:
        return ''
    return jdatetime.date.fromgregorian(date=value).strftime('%Y/%m/%d')


def gregorian_datetime_to_jalali_string(value):
    if not value:
        return ''
    utc_dt = value.replace(tzinfo=ZoneInfo('UTC'))
    tehran_dt = utc_dt.astimezone(ZoneInfo('Asia/Tehran'))
    return jdatetime.datetime.fromgregorian(datetime=tehran_dt).strftime('%Y/%m/%d %H:%M')


def parse_jalali_date(date_text):
    if not date_text:
        return None

    cleaned = date_text.strip().replace('-', '/')
    year, month, day = cleaned.split('/')
    jalali_date = jdatetime.date(int(year), int(month), int(day))
    return jalali_date.togregorian()
