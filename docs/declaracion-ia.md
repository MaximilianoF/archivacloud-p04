# Anexo A — Declaración detallada de uso de IA
Pareja: P-04  
Integrante: Maximiliano Ferrari  

| # | Fecha | Herramienta | Prompt usado | Cómo se validó |
|---|-------|-------------|--------------|----------------|
| 1 | 11/06/2026 | Claude | Cómo crear un bucket S3 en AWS Academy y configurar región | Se verificó que el bucket quedó creado en la consola de AWS |
| 2 | 11/06/2026 | Claude | Generar código base de FastAPI con endpoint POST presigned-url usando boto3 | Se probó el endpoint en /docs y retornó código 200 |
| 3 | 11/06/2026 | Claude | Cómo configurar CORS en FastAPI para permitir solo localhost:5173 | Se verificó que el frontend conecta sin errores CORS |
| 4 | 12/06/2026 | Claude | Cómo corregir error de indentación en main.py | Se ejecutó el servidor y no hubo errores |
| 5 | 12/06/2026 | Claude | Cómo leer el archivo .env desde una ruta relativa en FastAPI | Se verificó que las variables de entorno se cargan correctamente |
| 6 | 18/06/2026 | Claude | Cómo agregar barra de progreso en axios con onUploadProgress | Se probó subiendo un archivo y la barra apareció correctamente |
| 7 | 19/06/2026 | Claude | Cómo mejorar mensajes de error en FastAPI sin exponer stack traces | Se verificó que los errores retornan mensajes genéricos |
| 8 | 19/06/2026 | Claude | Cómo ejecutar pip-audit y npm audit y qué hacer con los resultados | Se ejecutaron ambos comandos y se corrigió la vulnerabilidad de npm |
| 9 | 09/07/2026 | Claude | Cómo integrar DynamoDB con boto3 en FastAPI para registrar subidas | Se verificó que al subir un archivo aparece el registro en la tabla |

**Firma:** Maximiliano Ferrari