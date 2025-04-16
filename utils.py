import qrcode
import os

def generar_qr_residente(residente_id: int):
    datos = f"ID del residente: {residente_id}"
    qr = qrcode.make(datos)

    carpeta = "qr_residentes"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    filename = os.path.join(carpeta, f"qr_residente_{residente_id}.png")
    qr.save(filename)
    return filename
