# json decode strings as ascii instead of unicode

def decode_dict(dct):
    newdict = {}
    for k, v in dct.items():
        if isinstance(k, bytes):
            k = k.encode('utf-8')
        if isinstance(v, bytes):
             v = v.encode('utf-8')
        elif isinstance(v, list):
            v = _decode_list(v)
        newdict[k] = v
    return newdict

def _decode_list(lst):
    newlist = []
    for i in lst:
        if isinstance(i, dict):
            i = i.encode('utf-8')
        elif isinstance(i, list):
            i = _decode_list(i)
        newlist.append(i)
    return newlist
