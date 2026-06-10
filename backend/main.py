from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
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

@app.get("/api/files")
def listar_archivos():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix="uploads/")
        archivos = []
        for obj in response.get("Contents", []):
            archivos.append({
                "nombre": obj["Key"].replace("uploads/", ""),
                "key": obj["Key"],
                "tamaño": obj["Size"],
                "fecha": obj["LastModified"].strftime("%Y-%m-%d %H:%M"),
                "url": s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": BUCKET, "Key": obj["Key"]},
                    ExpiresIn=3600,
                )
            })
        return archivos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al listar archivos")

@app.delete("/api/files/{key:path}")
def eliminar_archivo(key: str):
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
        return {"mensaje": "Archivo eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar archivo")