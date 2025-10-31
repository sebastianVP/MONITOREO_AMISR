import pandas as pd

# === CONFIGURACIÓN ===
# Ruta del archivo CSV
ruta_csv = "revision_mensual_avp_2025.csv"  # Cambia esto si tu archivo tiene otro nombre
ruta_csv = "temporal_reporte.csv"
# === LECTURA DEL CSV ===
try:
    df = pd.read_csv(ruta_csv)
except FileNotFoundError:
    print(f"❌ No se encontró el archivo: {ruta_csv}")
    exit()

# === LIMPIEZA Y VALIDACIÓN ===
# Aseguramos que las columnas clave existan
columnas_esperadas = {'FECHA', 'TIPO', 'SIZE (GB)', 'HORAS'}
if not columnas_esperadas.issubset(df.columns):
    print("❌ El archivo CSV no contiene las columnas esperadas:", columnas_esperadas)
    exit()

# Convertimos horas a numérico por si acaso
df['HORAS'] = pd.to_numeric(df['HORAS'], errors='coerce').fillna(0)

# === AGRUPACIÓN POR TIPO ===
resumen = df.groupby('TIPO')['HORAS'].sum()

horas_isr = resumen.get('isr', 0)
horas_esf = resumen.get('esf', 0)
total_horas = horas_isr + horas_esf

# === RESULTADOS ===
print("📊 RESUMEN DE HORAS ACUMULADAS")
print("=" * 35)
print(f"Total horas ISR : {horas_isr:.2f} h")
print(f"Total horas ESF : {horas_esf:.2f} h")
print(f"-------------------------------")
print(f"TOTAL GENERAL   : {total_horas:.2f} h")

# === OPCIONAL: Guardar resumen en CSV ===
resumen_df = pd.DataFrame({
    'TIPO': ['isr', 'esf', 'TOTAL'],
    'HORAS': [horas_isr, horas_esf, total_horas]
})
resumen_df.to_csv("resumen_horas.csv", index=False)
print("\n✅ Resumen guardado en 'resumen_horas.csv'")
