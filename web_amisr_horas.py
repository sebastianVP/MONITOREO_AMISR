import smtplib
import requests
from bs4 import BeautifulSoup
import re
import json
from email.message import EmailMessage
"""
🔒 1. Activa la verificación en dos pasos completamente
Ve a 👉 https://myaccount.google.com/security

En "Inicio de sesión en Google", activa completamente la verificación en dos pasos.

Termina el proceso, usando tu número de teléfono o la app Authenticator.

🔓 2. Accede a “Contraseñas de aplicación”
Una vez activada la verificación en dos pasos, vuelve a:

👉 https://myaccount.google.com/apppasswords

Ahí podrás:

Seleccionar aplicación: Correo

Dispositivo: Otro (por ejemplo, Python-script)

Se generará una contraseña de 16 caracteres (algo como: abcd efgh ijkl mnop)
"""


# 1. URL de la página que contiene el bloque de JavaScript con los datos
url = "http://127.0.0.1:8000/"  # <-- Reemplaza con la URL real

# 2. Obtener contenido HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 3. Buscar el bloque JavaScript que contiene 'let data = {...};'
script_tags = soup.find_all("script")
data_script = None

for script in script_tags:
    if "let data = " in script.text:
        data_script = script.text
        break

# 4. Extraer el bloque JSON de 'let data = {...};'
match = re.search(r"let\s+data\s*=\s*(\{.*?\});", data_script, re.DOTALL)

if match:
    js_object = match.group(1)
    
    # 5. Convertir a formato JSON válido (reemplazando posibles detalles de JS)
    js_object = js_object.replace(";", "")  # Eliminar punto y coma si está
    data_dict = json.loads(js_object)

    # 6. Extraer y procesar la lista de horas
    dias       = data_dict["dias"]
    horas      = data_dict["horas"]
    suma_horas = sum(horas)
    cantidad   = len(horas)
    resultado  = suma_horas / (cantidad * 24)

    # --- Extraer mes y año del HTML ---
    # Buscar <option selected> en el select de año y mes
    mes_select = soup.find("select", {"id": "mes"})
    anio_select = soup.find("select", {"id": "anio"})

    mes = mes_select.find("option", selected=True).text if mes_select else "Mes no encontrado"
    print("MES: ",mes)
    anio = anio_select.find("option", selected=True).text if anio_select else "Año no encontrado"

    # Último día grabado
    ultimo_dia = max(dias)

    # 7. Mostrar resultados
    print("✅ Lista de horas:", horas)
    print("🔢 Cantidad de elementos:", cantidad)
    print("🧮 Suma total de horas:", round(suma_horas, 2))
    print("📊 % Operacion (suma / (n * 24) ):", round(resultado,2)*100)

    # 8. Construir el mensaje ---
    mensaje = f"""\
    REPORTE  DE OPERACION RADAR AMISR-14

    📅 Información correspondiente a: {mes} {anio}
    📌 Último día registrado: {ultimo_dia} de {mes}

    ✅ Lista de horas: {horas}
    🔢 Cantidad de elementos: {cantidad}
    🧮 Suma total de horas: {round(suma_horas, 2)}
    📊 % Operacion (suma / (n * 24)): {round(resultado,2)*100}"""

    # 9. Enviar correo ---
    remitente    = "alexvaldez900@gmail.com"
    destinatario = "avaldez@igp.gob.pe"
    contraseña   = "mbjz opll bcta wykc"

    msg = EmailMessage()
    msg.set_content(mensaje)
    msg["Subject"] = "Resultados del procesamiento de datos del radar"
    msg["From"] = remitente
    msg["To"] = destinatario

    # Configuración para Gmail (puedes usar otros servidores SMTP si deseas)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, contraseña)
        smtp.send_message(msg)

    print("✅ Correo enviado con éxito.")

else:
    print("❌ No se encontró el bloque 'let data = {...};'")
