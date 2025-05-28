from fastapi.responses import Response
import orjson

def orjson_dumps(v, *, default=None):
    # orjson.dumps returns bytes, need to decode to string
    return orjson.dumps(v, default=default, option=orjson.OPT_INDENT_2).decode()

class CustomJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(
            content,
            option=orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE | orjson.OPT_SERIALIZE_NUMPY
        )
