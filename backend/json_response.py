from fastapi.responses import Response
import json

class FormattedJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        """Render the response content with proper JSON formatting."""
        return json.dumps(
            content,
            indent=2,
            separators=(',', ': '),
            ensure_ascii=False,
            sort_keys=False
        ).encode('utf-8')
