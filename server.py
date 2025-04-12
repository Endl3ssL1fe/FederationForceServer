import socket
import threading
import struct

HOST = '0.0.0.0'  
PORT = 30000       

def handle_authentication(conn):
    challenge = b'\x01\x02\x03\x04'  
    conn.sendall(challenge)

    response = conn.recv(1024)
    if response == b'\x04\x03\x02\x01':  
        return True
    else:
        return False

def handle_packet(data):
    packet_type = data[0]

    if packet_type == 0x01:
        response = b'\x01\x01'  
    else:
        response = b'\x00\x00'  

    return response

def handle_client(conn, addr):
    if not handle_authentication(conn):
        conn.close()
        return

    while True:
        data = conn.recv(1024)
        if not data:
            break
        response = handle_packet(data)
        conn.sendall(response)

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_server()

