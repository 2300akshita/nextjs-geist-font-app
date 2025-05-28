from fastapi.responses import JSONResponse
import json
import orjson

class CustomJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content) -> bytes:
        """Custom JSON rendering that ensures proper formatting."""
        # Use orjson for better JSON serialization
        return orjson.dumps(
            content,
            option=orjson.OPT_INDENT_2 | orjson.OPT_SERIALIZE_NUMPY
        )

    @staticmethod
    def format_json(data):
        """Helper method to format JSON with proper commas."""
        if isinstance(data, dict):
            return {k: CustomJSONResponse.format_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [CustomJSONResponse.format_json(item) for item in data]
        else:
            return data
