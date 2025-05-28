from fastapi import FastAPI
from fastapi.responses import Response
import json

app = FastAPI()

@app.get("/test")
async def test_endpoint():
    data = {
        "key1": "value1",
        "key2": "value2",
        "array": [1, 2, 3],
        "nested": {
            "inner": "value"
        }
    }
    
    # Format JSON with explicit commas and newlines
    json_str = json.dumps(data, indent=2, ensure_ascii=False, separators=(',', ': '))
    
    # Add explicit content-type header
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Content-Type-Options": "nosniff"
    }
    
    return Response(
        content=json_str.encode('utf-8'),
        media_type="application/json",
        headers=headers
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
