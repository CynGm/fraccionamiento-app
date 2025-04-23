import qrcode
import os
from fastapi.responses import FileResponse
from fastapi import HTTPException

CARPETA_QR = "qr_residentes"

if not os.path.exists(CARPETA_QR):
    os.makedirs(CARPETA_QR)

def generar_qr_residente(residente_id: int):
    datos = f"ID del residente: {residente_id}"
    qr = qrcode.make(datos)
    nombre_archivo = f"qr_residente_{residente_id}.png"
    ruta_archivo = os.path.join(CARPETA_QR, nombre_archivo)
    qr.save(ruta_archivo)

def descargar_qr(residente_id: int):
    nombre_archivo = f"qr_residente_{residente_id}.png"
    ruta_archivo = os.path.join(CARPETA_QR, nombre_archivo)

    if not os.path.exists(ruta_archivo):
        raise HTTPException(status_code=404, detail="QR no encontrado para este residente.")

    return FileResponse(
        path=ruta_archivo,
        media_type="image/png"
    )
