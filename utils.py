import qrcode
import base64
from io import BytesIO
import os

def generar_qr_residente(residente_id: int) -> str:
    # Contenido del QR
    data = f"residente_{residente_id}"
    
    # Crear el QR
    qr = qrcode.make(data)
    
    # Guardar imagen en memoria para codificarla en base64
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Crear carpeta si no existe
    ruta_directorio = "qr_residentes"
    os.makedirs(ruta_directorio, exist_ok=True)

    # Ruta para guardar archivo físico
    ruta_archivo = os.path.join(ruta_directorio, f"qr_residente_{residente_id}.png")
    with open(ruta_archivo, "wb") as f:
        f.write(buffer.getvalue())

    # Codificar imagen como base64
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return imagen_base64



