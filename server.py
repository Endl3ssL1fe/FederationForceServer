import socket
import threading

# === CONFIG ===
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 30000       # Default port for Federation Force (change if needed)

# === Basic Server Setup ===
def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[>] Received: {data.hex()}")
            response = b'\x00'  # Placeholder response
            conn.sendall(response)
    except Exception as e:
        print(f"[!] Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed")

def start_server():
    print("[*] Starting server...")  # Added this for debugging
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[*] Connection accepted from {addr}")  # Added this for debugging
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
