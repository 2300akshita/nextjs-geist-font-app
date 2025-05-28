import json
from typing import Any

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that ensures proper formatting."""
    
    def default(self, obj: Any) -> Any:
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)
    
    def encode(self, obj: Any) -> str:
        """Override encode method to ensure proper formatting."""
        return json.dumps(
            obj,
            indent=2,
            separators=(',', ': '),
            ensure_ascii=False,
            cls=CustomJSONEncoder
        )

def custom_dumps(obj: Any) -> str:
    """Helper function to use the custom encoder."""
    return CustomJSONEncoder().encode(obj)
