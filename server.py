import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 8
SERVER_FOLDER = 'server_data'


def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")

    """ Server has accepted the connection from the client. """
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        """ Receiving the filename from the client. """
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Requested {filename}.")

        """ Sending file to client """
        with open(f"server_data/files/{filename}", "rb") as file:
            data = file.read()
            data += b'EOF'
            conn.sendall(data)
            print(f'[SERVER] File {filename} sent.')

    """ Closing the connection from the server. """
    server.close()
    print('[SERVER] server closed.')


if __name__ == '__main__':
    main()

