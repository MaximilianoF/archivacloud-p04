# Reporte de Seguridad — ArchivaCloud P-04

Pareja: P-04  
Integrante: Maximiliano Ferrari  
Fecha: 09/07/2026  

## SEC-01 — Secretos fuera del repositorio
Las credenciales AWS se almacenan en el archivo `.env` que está incluido en `.gitignore`. El repositorio solo contiene `.env.example` con placeholders. Se verificó que ningún commit contiene credenciales reales.

## SEC-02 — CORS restrictivo
El backend FastAPI configura CORS permitiendo únicamente el origen `http://localhost:5173`. No se usa comodín `*`.

## SEC-03 — Validación de entrada
Se usa Pydantic para validar el cuerpo de cada request. Las extensiones permitidas son únicamente `csv` y `xlsx`, validadas mediante lista blanca. El fileName se sanitiza extrayendo solo la extensión.

## SEC-04 — Límite de tamaño
El backend rechaza archivos mayores a 25 MB. El frontend también filtra antes de enviar la request.

## SEC-05 — IAM mínimo privilegio
La política IAM permite únicamente 4 acciones: `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, `s3:ListBucket`, aplicadas solo sobre el bucket `archivacloud-p04-ferrari`. No se usan comodines en acciones ni recursos.

## SEC-06 — S3 cerrado al público
El bucket tiene Block Public Access activado en todas sus opciones. No existe bucket policy permisiva.

## SEC-07 — Errores sin información sensible
Los bloques `except` del backend retornan solo mensajes genéricos como "Error interno del servidor". No se exponen stack traces ni detalles técnicos al cliente.

## SEC-08 — Encriptación en reposo
El bucket S3 tiene SSE-S3 activado como cifrado por defecto en todos los objetos almacenados.

## SEC-09 — Escaneo de dependencias
Se ejecutó `python -m pip_audit` en el backend. Los paquetes del proyecto no presentaron vulnerabilidades. Se ejecutó `npm audit` en el frontend, se detectó 1 vulnerabilidad high en form-data corregida con `npm audit fix`. Resultado final: 0 vulnerabilidades en ambos.

## SEC-10 — TLS de extremo a extremo
Todas las llamadas a S3 utilizan HTTPS mediante presigned URLs generadas por boto3. En producción se debe desplegar el backend detrás de un proxy con certificado TLS (nginx + certbot o AWS ALB con ACM).