import pytz
from datetime import datetime
from dateutil import parser
from pytz import timezone, UTC
from marshmallow import ValidationError


def timezone_converter(date_input, **kwargs):
    """
    This function convert date strings in a dict, a list or a str in any format
    to a defined format and defined timezone

    Args:
        - date_input (str, list, dict): Input, may be a list, a dict or a str
        - time_format (str): Expected format, default: %Y-%m-%d %H:%M:%S
        - tz (str): Expected timezone. Ex: Asia/Ho_Chi_Minh
        - valid_keys (list): Just convert these keys

    Return:
        The date_input after convertation

    Raise:
    """
    def _str_converter(date_str, **kwargs):
        keep = kwargs.get('keep', False)
        if keep:
            return date_str

        time_format = '%Y-%m-%d %H:%M:%S'

        date_time = parser.parse(date_input)

        if not date_time.tzinfo:
            date_time = date_time.replace(tzinfo=UTC)

        if kwargs.get('time_format'):
            time_format = kwargs['time_format']

        if kwargs.get('tz'):
            tz = kwargs['tz']
            date_time = date_time.astimezone(timezone(tz))

        output = datetime.strftime(date_time, time_format)

        return output

    def _dict_converter(date_dict, **kwargs):
        valid_keys = kwargs.get('valid_keys')

        for key, value in date_input.items():
            kwargs['keep'] = not (valid_keys and key in valid_keys)
            date_input[key] = timezone_converter(value, **kwargs)
        return date_input

    if isinstance(date_input, str):
        return _str_converter(date_input, **kwargs)
    elif isinstance(date_input, dict):
        return _dict_converter(date_input, **kwargs)
    elif isinstance(date_input, list):
        return [
            timezone_converter(e, **kwargs) for e in date_input
        ]
    else:
        return date_input


def iso_convert(date_string, is_utc=True):
    if not date_string:
        return date_string
    try:
        utc_time = datetime.fromisoformat(
            date_string
        )
        if is_utc:
            utc_time = utc_time.astimezone(pytz.utc)
        return utc_time
    except Exception:
        raise ValidationError('Invalid format date')
