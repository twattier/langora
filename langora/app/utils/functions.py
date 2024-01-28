
from datetime import datetime
from dateutil import tz

def list_to_string(list:list, sep=", ")->str:
    txt = ""
    for item in list:
        if txt!="": txt += sep
        txt += item
    return txt

def string_to_list(txt:str, sep=",")->list:
    parts = txt.split(sep)
    list = []
    for part in parts:
        list.append(part.strip())
    return list

def list_obj_attribute(list:list, attribute_name:str)->list:
    attrs = []
    for item in list:
        attrs.append(getattr(item, attribute_name))
    return attrs

def args_to_string(args, sep=", "):
    txt = ""
    for arg in args:
        if txt != "":
            txt += sep
        if isinstance(arg, str):
            txt += "'" + str(arg) + "'"
        else:
            txt += str(arg)
    return txt

def utc_to_tz(dt:datetime)->datetime:
    if not dt:
        return None
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    dt_utc = dt.replace(tzinfo=from_zone)
    return dt_utc.astimezone(to_zone)

def get_url_hostname(url:str):
    from urllib.parse import urlparse
    parse = urlparse(url)
    return parse.hostname