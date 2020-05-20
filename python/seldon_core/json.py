from json import JSONEncoder, dumps


class JSONEncoderForHTML(JSONEncoder):
    """
    An encoder that escapes JSON to prevent XSS injections.
    That is, it escapes certain HTML characters.
    https://github.com/SeldonIO/seldon-core/issues/837

    Adapted from `simplejson`'s implementation of JSONEncoderForHTML:
    https://github.com/simplejson/simplejson/blob/master/simplejson/encoder.py
    """

    def default(self, o):
        return super().default(o)

    def iterencode(self, o, _one_shot=False):
        chunks = super().iterencode(o, _one_shot)
        for chunk in chunks:
            chunk = chunk.replace("&", "\\u0026")
            chunk = chunk.replace("<", "\\u003c")
            chunk = chunk.replace(">", "\\u003e")

            if not self.ensure_ascii:
                chunk = chunk.replace(u"\u2028", "\\u2028")
                chunk = chunk.replace(u"\u2029", "\\u2029")

            yield chunk


def htmlescape_dumps(o, **kwargs):
    """
    Wrapper around `json.dumps` which ensures that some of the HTML characters
    in the JSON output are escaped, to prevent XSS injections.
    https://github.com/SeldonIO/seldon-core/issues/837
    """
    kwargs["cls"] = JSONEncoderForHTML
    return dumps(o, **kwargs)
