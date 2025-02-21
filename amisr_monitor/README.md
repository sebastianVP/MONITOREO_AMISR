# PAGINA DE MONITOREO DE DATOS AMISR-14
---
1. Creación de pagina en Django.
2. En la pc tenemos:
    - cd /home/soporte/
    - mkdir WEBPAGE_AMISR_14
    - python -m venv webpage_amisr_env
    - source  webpage_amisr_env/bin/activate
    - git clone git@github.com:sebastianVP/MONITOREO_AMISR.git
    - cd MONITOREO_AMISR
    - Instalar DJango y otras dependencias: pip install django pandas matplotlib seaborn
    - Crear proyecto Django: django-admin startproject amisr_monitor
    - cd amisr_monitor
    - python -m pip freeze > requirements.txt
    - nano README.md
    - Crear una aplicacion dentro del proyecto: python manage.py startapp monitoring

**3. Configurar Django y la aplicacion.**

- Configuracion previa
sudo locale-gen es_ES.UTF-8
sudo update-locale LANG=es_ES.UTF-8

- Crear la carpeta media
- cd /home/soporte/WEBPAGE_AMISR_14/MONITOREO_AMISR/amisr_monitor
- mkdir media
Registrar la aplicacin en settings.py

# Nota
En caso el puerto se encuentre ubicado ejecutar los siguientes comandos:
```
(webpage_amisr_env) soporte@CI-91:~/WEBPAGE_AMISR_14/MONITOREO_AMISR/amisr_monitor$ python manage.py  runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Error: That port is already in use.
(webpage_amisr_env) soporte@CI-91:~/WEBPAGE_AMISR_14/MONITOREO_AMISR/amisr_monitor$ sudo lsof -i :8000
[sudo] password for soporte: 
COMMAND   PID    USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
python  29134 soporte    4u  IPv4 9348696      0t0  TCP localhost:8000 (LISTEN)
(webpage_amisr_env) soporte@CI-91:~/WEBPAGE_AMISR_14/MONITOREO_AMISR/amisr_monitor$ sudo kill -9 29134
(webpage_amisr_env) soporte@CI-91:~/WEBPAGE_AMISR_14/MONITOREO_AMISR/amisr_monitor$ python manage.py  runserver
```



