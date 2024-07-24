import subprocess

def verify_online(ip):
    # Tenta enviar um ping para o IP alvo
    process = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        return True
    else:
        return False

# import socket

# def verify_online(ip):
#     try:
#         socket.create_connection((ip, 80), timeout=1)
#         return True
#     except OSError:
#         return False