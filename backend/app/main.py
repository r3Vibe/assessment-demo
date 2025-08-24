"""FastAPI Wrapper"""

import logging

from fastapi import FastAPI, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.sockets import app as sio_app

# setup logger
logger = logging.getLogger("uvicorn.error")

# setup FastAPI app
app = FastAPI(
    title="BatLabs Agent",
    description="A FastAPI wrapper for Ai Agent for BatLabs",
    version="1.0.0",
)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount the socket.io
app.mount("/socket.io", sio_app)

# Define API endpoints


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"data": "Server is running"}


@app.post("/upload")
async def upload_file(file: UploadFile):
    file_ext = file.filename.split(".")[-1]
    if file_ext != "csv":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV Files Are Allowed"
        )

    import os
    import uuid

    file_path = os.path.join("app", "data")
    os.makedirs(file_path, exist_ok=True)
    final_name = f"{uuid.uuid4()}.{file_ext}"
    final_path = os.path.join(file_path, final_name)

    with open(final_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully.", "location": final_name}
