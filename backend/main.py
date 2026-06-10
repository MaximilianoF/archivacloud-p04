from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)

BUCKET = os.getenv("S3_BUCKET_NAME")
ALLOWED_EXTENSIONS = {"csv", "xlsx"}
MAX_SIZE_MB = 25

class PresignedRequest(BaseModel):
    fileName: str
    fileType: str
    fileSize: int

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/api/upload/presigned-url")
def get_presigned_url(req: PresignedRequest):
    ext = req.fileName.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
    if req.fileSize > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande")
    key = f"uploads/{req.fileName}"
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": req.fileType},
        ExpiresIn=300,
    )
    return {"presignedUrl": url, "key": key}