from fastapi import FastAPI, Response
import json

app = FastAPI()

@app.post("/test")
async def test_endpoint():
    data = {
        "name": "Test",
        "values": [1, 2, 3],
        "nested": {
            "key": "value"
        }
    }
    # Format JSON with explicit commas and proper indentation
    json_str = '{\n'
    json_str += '  "name": "Test",\n'
    json_str += '  "values": [\n'
    json_str += '    1,\n'
    json_str += '    2,\n'
    json_str += '    3\n'
    json_str += '  ],\n'
    json_str += '  "nested": {\n'
    json_str += '    "key": "value"\n'
    json_str += '  }\n'
    json_str += '}'

    return Response(
        content=json_str,
        media_type="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
