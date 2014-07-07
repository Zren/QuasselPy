import logging
import json
import functools

def json_default(obj):
    import calendar, datetime
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis

    return dict(obj)

def jsonify(data, sort_keys=True):
    return json.dumps(data, sort_keys=sort_keys, indent=2, default=json_default) #lambda data: dict(data))

def prettyprint(data, sort_keys=True):
    print(prettify(data, sort_keys))

def logPretty(obj):
    logDebug(prettify(obj))

def logDebug(msg, *args, **kwargs):
    logging.log(logging.DEBUG, msg, *args, **kwargs)

def logRequest(r, *args, **kwargs):
    logDebug(r.url)
    logPretty(r.request.headers)
    logPretty(r.headers)
    try:
        logPretty(r.json())
    except: # JSONDecodeError
        logDebug(r.text)

def listify(f):
    @functools.wraps(f)
    def listify_helper(*args, **kwargs):
        return list(f(*args, **kwargs))
    return listify_helper
