import qrcode
import os

def generar_qr_residente(id_residente: int):
    contenido = f"residente_id:{id_residente}"
    qr = qrcode.make(contenido)

    ruta_carpeta = "qr_residentes"
    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_archivo = os.path.join(ruta_carpeta, f"residente_{id_residente}.png")
    qr.save(ruta_archivo)

    return ruta_archivo
