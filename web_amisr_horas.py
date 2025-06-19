import requests
from bs4 import BeautifulSoup
import re
import json

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
    horas = data_dict["horas"]
    suma_horas = sum(horas)
    cantidad = len(horas)
    resultado = suma_horas / (cantidad * 24)

    # 7. Mostrar resultados
    print("✅ Lista de horas:", horas)
    print("🔢 Cantidad de elementos:", cantidad)
    print("🧮 Suma total de horas:", round(suma_horas, 2))
    print("📊 % Operacion (suma / (n * 24) ):", round(resultado, 4)*100)

else:
    print("❌ No se encontró el bloque 'let data = {...};'")
