
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
        param = part.strip()
        if len(param)>0:
            list.append(param)
    return list

def list_obj_attribute(list:list, attribute_name:str)->list:
    attrs = []
    for item in list:
        attrs.append(getattr(item, attribute_name))
    return attrs

def split_list(lst:list, n):
    splits = []
    for i in range(0, len(lst), n):
        splits.append(lst[i:i + n])
    return splits

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

def string_to_args(txt:str, sep=", "):
    list = []
    idxb = txt.find('[')
    if idxb > 0:
        beg = string_to_args(txt[:idxb])
        if len(beg)>0:
            list.extend(beg)
    if idxb>=0:
        idxe = txt.rfind(']', idxb)
        tab = txt[idxb+1:idxe]
        list.append(string_to_args(tab))
        if idxe+1 < len(txt):
            end = string_to_args(txt[idxe+1:])
            if len(end)>0:
                list.extend(end)
    else:
        return string_to_list(txt)
    return list

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