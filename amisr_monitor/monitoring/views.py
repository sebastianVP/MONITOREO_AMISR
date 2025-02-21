from django.shortcuts import render

# Create your views here.
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Desactiva GUI para evitar errores en servidor
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import locale

# Establecer el idioma español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

# Cargar el CSV en un DataFrame
def load_data():
    #file_path = os.path.join(settings.BASE_DIR, 'data', 'reporte_tamanos_directorios.csv')
    df = pd.read_csv("https://raw.githubusercontent.com/sebastianVP/DATASETS_CLASE/refs/heads/main/reporte_tamanos_directorios.csv")
    print(df.head())
    df['Dia'] = pd.to_datetime(df['Dia'], format='%Y%m%d')  # Convertir a formato de fecha
    df['Mes'] = df['Dia'].dt.strftime('%B').str.capitalize()  # Extraer nombre del mes en espanol
    df['Año'] = df['Dia'].dt.year  # Extraer el año
    return df

def home(request):
    df = load_data()
    meses = df['Mes'].unique()
    anios = df['Año'].unique()
    print("anio",anios)
    #print("0",anios[0])
    print("meses",meses)
    print("meses",meses[-1])
    try:
        # selected_month = request.GET.get('mes', meses[0] if meses else 'Enero')
        selected_year = int(request.GET.get('anio', anios[-1] if anios.size > 0 else pd.Timestamp.now().year))
        selected_month = request.GET.get('mes', meses[-1] if len(meses) > 0 else 'Enero')
        print("selected_year",selected_year)
        print("selected_month",selected_month)

    except:
        print("Error")

    df_filtered = df[(df['Año'] == selected_year) & (df['Mes'] == selected_month)]
    # Si el DataFrame está vacío, agregar un valor por defecto
    if df_filtered.empty:
        df_filtered = pd.DataFrame({
            'Dia': [pd.Timestamp(f'{selected_year}-{pd.to_datetime(selected_month, format="%B").month:02d}-01')],
            'Tamano_GB': [0.0],
            'Horas': [0.0],
            'Mes': [selected_month],
            'Año': [selected_year]
        })
    print("STEP 2")
    #df_filtered = df[df['Mes'] == selected_month]
    print("df_filtered",df_filtered)
    #   Calcular porcentaje de operación
    total_dias = df_filtered['Dia'].nunique()
    total_horas_posibles = total_dias * 24
    total_horas_grabadas = df_filtered['Horas'].sum()
    if total_horas_posibles > 0:
        porcentaje_operacion = (total_horas_grabadas / total_horas_posibles) * 100
    else:
        porcentaje_operacion = 0



    porcentaje_operacion = (total_horas_grabadas / total_horas_posibles) * 100 if total_horas_posibles > 0 else 0
    # Generar gráfico de horas grabadas
    plt.figure(figsize=(10, 5))
    sns.set_style("darkgrid")  # Agregar estilo visual atractivo
    ax = sns.barplot(x=df_filtered['Dia'].dt.day, y=df_filtered['Horas'], palette='viridis')
    plt.xlabel('Día')
    plt.ylabel('Horas Grabadas')
    plt.title(f'Horas Grabadas en {selected_month} {selected_year} ({porcentaje_operacion:.2f}% de operación)')
    
    # Agregar etiquetas a las barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    
    plt.xticks(rotation=45)
    horas_path = os.path.join(settings.MEDIA_ROOT, 'horas_grabadas.png')
    plt.savefig(horas_path)
    plt.close()
    
    # Generar gráfico de tamaño en GB
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=df_filtered['Dia'].dt.day, y=df_filtered['Tamano_GB'], palette='Blues')
    plt.xlabel('Día')
    plt.ylabel('Tamaño (GB)')
    plt.title(f'Tamaño de Datos en {selected_month} {selected_year}')
    
    # Agregar etiquetas a las barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    
    plt.xticks(rotation=45)
    tamano_path = os.path.join(settings.MEDIA_ROOT, 'tamano_datos.png')
    plt.savefig(tamano_path)
    plt.close()

    # Generar gráfico de porcentaje de almacenamiento
    if total_horas_posibles > 0:
        almacenado = max(0, total_horas_grabadas)
        no_almacenado = max(0, total_horas_posibles - total_horas_grabadas)
        sizes = [almacenado, no_almacenado]
    else:
        sizes = [1, 0]  # Evitar error en el gráfico si no hay datos
    plt.figure(figsize=(6, 6))
    print("TOTAL_HORAS_POSIBLES",total_horas_posibles)
    print("TOTAL_HORAS_GRABADAS",total_horas_grabadas)
    sizes = [total_horas_grabadas, total_horas_posibles - total_horas_grabadas]
    labels = ['Almacenado', 'No Almacenado']
    colors = ['#4caf50', '#f44336']
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, counterclock=False)
    plt.title(f'Porcentaje de Almacenamiento en {selected_month} {selected_year}\n (Total días registrados: {total_dias})', fontsize=12)
    porcentaje_path = os.path.join(settings.MEDIA_ROOT, 'porcentaje_almacenamiento.png')
    plt.savefig(porcentaje_path)
    plt.close()
    """
    # Generar gráfico de horas grabadas
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df_filtered['Dia'].dt.day, y=df_filtered['Horas'], hue=df_filtered['Dia'].dt.day, palette='coolwarm', legend=False)
    plt.xlabel('Día')
    plt.ylabel('Horas Grabadas')
    plt.title(f'Horas Grabadas en {selected_month}')
    #print("MEDIA_ROOT",settings.MEDIA_ROOT)
    horas_path = os.path.join(settings.MEDIA_ROOT, 'horas_grabadas.png')
    plt.savefig(horas_path)
    plt.close()
    
    # Generar gráfico de tamaño en GB
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df_filtered['Dia'].dt.day, y=df_filtered['Tamano_GB'], hue=df_filtered['Dia'].dt.day, palette='Blues', legend=False)
    plt.xlabel('Día')
    plt.ylabel('Tamaño (GB)')
    plt.title(f'Tamaño de Datos en {selected_month}')
    tamano_path = os.path.join(settings.MEDIA_ROOT, 'tamano_datos.png')
    plt.savefig(tamano_path)
    plt.close()
    """
    return render(request, 'monitoring/home.html', {
        'df': df_filtered.to_dict(orient='records'), 
        'meses': meses,
        'anios': anios,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'horas_grafico': f"{settings.MEDIA_URL}horas_grabadas.png",
        'tamano_grafico': f"{settings.MEDIA_URL}tamano_datos.png",
        'porcentaje_grafico': f"{settings.MEDIA_URL}porcentaje_almacenamiento.png"
    })

def descargar_csv(request,anio, mes):
    df = load_data()
    #df_filtered = df[df['Mes'] == mes]
    df_filtered = df[(df['Mes'] == mes) & (df['Año'] == int(anio))]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="datos_{mes}.csv"'
    df_filtered.to_csv(response, index=False)
    return response