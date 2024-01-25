def list_to_string(list:list, sep=", "):
    txt = ""
    for item in list:
        if txt!="": txt += sep
        txt += item
    return txt

def get_url_hostname(url:str):
    from urllib.parse import urlparse
    parse = urlparse(url)
    return parse.hostname