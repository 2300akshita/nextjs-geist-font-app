from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
import json
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class CourseRequest(BaseModel):
    topic: str
    level: str
    days: int

@app.get("/")
async def read_root():
    """Serve the frontend HTML file"""
    return FileResponse("../frontend/index.html")

@app.post("/generate-course")
async def generate_course_endpoint(request: CourseRequest):
    """Generate a course based on the provided parameters."""
    try:
        logger.info(f"Generating course for topic: {request.topic}, level: {request.level}, days: {request.days}")
        
        # Generate course using our course generator
        from course_generator import generate_course
        course = await generate_course(request.topic, request.level, request.days)
        
        if not course:
            logger.error("Course generation returned None")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate course content. Please try again."
            )
            
        response = course.dict()
        logger.info("Course generated successfully")
        return JSONResponse(content=response)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error generating course: {error_msg}")
        
        if "AI generation failed" in error_msg:
            raise HTTPException(
                status_code=503,
                detail="AI service is temporarily unavailable. Please try again later."
            )
        elif "Invalid topic" in error_msg:
            raise HTTPException(
                status_code=400,
                detail="Invalid topic provided. Please try a different topic."
            )
        elif "Failed to parse" in error_msg:
            raise HTTPException(
                status_code=500,
                detail="Error processing course content. Please try again."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again later."
            )

# Serve static files
@app.get("/{path:path}")
async def serve_static(path: str):
    """Serve static files from the frontend directory"""
    if path == "":
        path = "index.html"
    file_path = f"../frontend/{path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("../frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
