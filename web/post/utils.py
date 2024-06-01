import os
import pytz
from web.settings import TIME_ZONE

# 更换时区
def convert_to_timezone(datetime_obj, timezone_str):
    target_timezone = pytz.timezone(timezone_str)
    converted_datetime = datetime_obj.astimezone(target_timezone)
    return converted_datetime.strftime('%Y-%m-%d %H:%M')