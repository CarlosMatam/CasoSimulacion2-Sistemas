import os
import datetime
import paramiko

# Definir la información de conexión al equipo remoto
ip = "192.168.1.18"  # Dirección IP del equipo remoto
usuario = "carlos"  # Nombre de usuario para la conexión SSH
contraseña = "Carlos9899"  # Contraseña para la conexión SSH

# Definir la información del directorio y el tiempo máximo de creación de archivos
directorio = "/home/carlos/practica2/"
tiempo_maximo_creacion = datetime.timedelta(days=1)

# Establecer la conexión SSH al equipo remoto
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=usuario, password=contraseña)

# Encontrar los archivos que cumplen los criterios de búsqueda
stdin, stdout, stderr = ssh.exec_command('find {} -type f -name ".log" -o -name ".txt" -ctime -{}'.format(directorio, tiempo_maximo_creacion.days))
archivos = stdout.read().splitlines()

# Comprimir los archivos encontrados en un archivo tar.gz
fecha_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_archivo = "respaldo_{}.tar.gz".format(fecha_actual)
comando = "tar czvf {} {}".format(nombre_archivo, " ".join(archivos))
stdin, stdout, stderr = ssh.exec_command(comando)

# Transferir el archivo comprimido al equipo local
sftp = ssh.open_sftp()
ruta_local = os.path.expanduser("C:\Users\prueb\OneDrive\Documents\respaldos")
sftp.put(nombre_archivo, os.path.join(ruta_local, nombre_archivo))

# Verificar que la transferencia se realizó correctamente y eliminar los archivos en el equipo remoto
if os.path.exists(os.path.join(ruta_local, nombre_archivo)):
    for archivo in archivos:
        ssh.exec_command('rm {}'.format(archivo))
        print("Archivo {} eliminado correctamente".format(archivo))
else:
    print("Error al transferir el archivo")

# Cerrar la conexión SSH
ssh.close()