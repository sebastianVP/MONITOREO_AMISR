# -*- coding: utf-8 -*-
"""
Script: revision_mensual_avp_2025.py
Autor: Alexander Valdez
Descripción:
    Escanea carpetas del radar AMISR y genera/acumula un reporte temporal con:
    FECHA, TIPO, SIZE (GB), HORAS
"""

import os
import subprocess
import csv

# === CONFIGURACIÓN ===
DATA_DIR = "/mnt/data_amisr"  # Ruta base del radar
DATA_DIR = "/media/soporte/Expansion/AMISR/2025"
OUTPUT_FILE = "temporal_reporte.csv"  # Archivo CSV acumulativo


# === FUNCIONES ===

def listar_carpetas_mes(base_dir, mes):
    """Lista carpetas con formato YYYYMMDD.xxx pertenecientes al mes indicado."""
    mes = str(mes).zfill(2)
    return sorted([
        c for c in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, c))
        and len(c) >= 8
        and c[:8].isdigit()
        and c[4:6] == mes
    ])


def obtener_tamano(carpeta_path):
    """Obtiene el tamaño con du -sh y devuelve valor en GB."""
    try:
        salida = subprocess.check_output(["du", "-sh", carpeta_path], text=True)
        size_str = salida.split()[0].strip()
        if size_str.lower().endswith("g"):
            return float(size_str[:-1])
        elif size_str.lower().endswith("m"):
            return float(size_str[:-1]) / 1000
        else:
            return 0.0
    except subprocess.CalledProcessError:
        return 0.0


def obtener_tipo(carpeta_path):
    """Busca archivo .exp dentro de Setup y devuelve las 3 primeras letras del nombre."""
    setup_dir = os.path.join(carpeta_path, "Setup")
    if not os.path.exists(setup_dir):
        return "N/A"
    for f in os.listdir(setup_dir):
        if f.endswith(".exp"):
            return f[:3].lower()
    return "N/A"


def calcular_horas(tipo, size_gb):
    """Calcula las horas según el tipo."""
    if "isr" in tipo:
        return round((11 * size_gb) / 59, 2)
    elif "esf" in tipo:
        return round((13 * size_gb) / 35, 2)
    else:
        return 0.0


def generar_registros(base_dir, mes):
    """Genera lista de registros (FECHA, TIPO, SIZE, HORAS)."""
    carpetas = listar_carpetas_mes(base_dir, mes)
    registros = []
    for carpeta in carpetas:
        fecha = carpeta[:8]
        carpeta_path = os.path.join(base_dir, carpeta)
        tipo = obtener_tipo(carpeta_path)
        size_gb = obtener_tamano(carpeta_path)
        horas = calcular_horas(tipo, size_gb)

        registros.append({
            "FECHA": fecha,
            "TIPO": tipo,
            "SIZE (GB)": round(size_gb, 2),
            "HORAS": horas
        })
    return registros


def cargar_csv_existente(output_file):
    """Lee los datos existentes del CSV (si lo hay)."""
    if not os.path.exists(output_file):
        return []
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def guardar_csv_acumulativo(nuevos, output_file):
    """Guarda los registros nuevos, acumulando con los existentes sin duplicar fechas."""
    existentes = cargar_csv_existente(output_file)
    fechas_existentes = {r["FECHA"] for r in existentes}

    nuevos_filtrados = [r for r in nuevos if r["FECHA"] not in fechas_existentes]

    if not nuevos_filtrados:
        print("\n⚠️ No se encontraron registros nuevos para agregar.")
        return

    # Unir todo
    todos = existentes + nuevos_filtrados

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["FECHA", "TIPO", "SIZE (GB)", "HORAS"])
        writer.writeheader()
        writer.writerows(todos)

    print(f"\n✅ {len(nuevos_filtrados)} registros nuevos añadidos a {output_file}")


def main():
    print("=== REVISIÓN MENSUAL AMISR ===")
    base_dir = input(f"Ingrese el directorio base (ENTER para usar {DATA_DIR}): ").strip() or DATA_DIR
    mes = input("Ingrese el número de mes (1-12): ").strip()

    if not mes.isdigit() or not (1 <= int(mes) <= 12):
        print("❌ Mes inválido.")
        return

    if not os.path.exists(base_dir):
        print(f"❌ El directorio {base_dir} no existe.")
        return

    registros = generar_registros(base_dir, mes)
    if not registros:
        print(f"⚠️ No se encontraron carpetas válidas para el mes {mes}.")
        return

    print("\n📋 Resultados del análisis:")
    for r in registros:
        print(f"  {r['FECHA']} | {r['TIPO']} | {r['SIZE (GB)']} GB | {r['HORAS']} h")

    guardar_csv_acumulativo(registros, OUTPUT_FILE)


# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    main()
