import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime

# === CONFIGURACIÓN ===
ruta_csv = "resumen_horas.csv"  # Archivo con columnas: TIPO, HORAS

# === LECTURA DEL CSV ===
try:
    df = pd.read_csv(ruta_csv)
except FileNotFoundError:
    print(f"❌ No se encontró el archivo: {ruta_csv}")
    exit()

# === OBTENER DATOS DEL CSV ===
horas_isr = float(df.loc[df['TIPO'] == 'isr', 'HORAS'].values[0]) if 'isr' in df['TIPO'].values else 0
horas_esf = float(df.loc[df['TIPO'] == 'esf', 'HORAS'].values[0]) if 'esf' in df['TIPO'].values else 0
total_horas = float(df.loc[df['TIPO'] == 'TOTAL', 'HORAS'].values[0]) if 'TOTAL' in df['TIPO'].values else horas_isr + horas_esf

# === INFORMACIÓN DE FECHA ===
fecha_actual = datetime.now()
mes = fecha_actual.strftime("%B").capitalize()
anio = fecha_actual.year

# === MENSAJE DE REPORTE ===
mensaje = f"""\
📡 REPORTE DE OPERACIÓN RADAR AMISR-14

📅 Información correspondiente a: {mes} {anio}

📊 RESUMEN DE HORAS ACUMULADAS
===================================
Total horas ISR : {horas_isr:.2f} h
Total horas ESF : {horas_esf:.2f} h
-----------------------------------
TOTAL GENERAL   : {total_horas:.2f} h

🗂️ Archivo adjunto: resumen_horas.csv
"""

# === CONFIGURACIÓN DE CORREO ===
remitente = "alexvaldez900@gmail.com"
destinatario = "avaldez@igp.gob.pe"
contraseña = "mbjz opll bcta wykc"  # Contraseña de aplicación Gmail

msg = EmailMessage()
msg["Subject"] = f"📡 Reporte de operación radar - {mes} {anio}"
msg["From"] = remitente
msg["To"] = destinatario
msg.set_content(mensaje)

# === ADJUNTAR ARCHIVO CSV ===
with open(ruta_csv, "rb") as f:
    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=ruta_csv)

# === ENVÍO DEL CORREO ===
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, contraseña)
        smtp.send_message(msg)
    print("✅ Correo enviado con éxito.")
except Exception as e:
    print("❌ Error al enviar el correo:", e)
