import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 8
SERVER_FOLDER = 'server_data'
DIR = 'server_data'


def main():
    """
    * Main function that initiates a TCP socket, binds the server and receives filenames from client
    * in order to send the corresponding files from the DIR = 'server_data' directory.
    """
    """ Staring a TCP socket. """
    print("[STARTING] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:

        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        while True:

            """ Receiving the filename from the client. """
            filename = conn.recv(SIZE).decode(FORMAT)
            if not filename:
                break
            print(f"[RECV] Requested {filename}.")

            """ Sending file to client """
            file_path = os.path.join(DIR, filename)
            with open(file_path, "rb") as file:
                data = file.read()
                data += b'2e51b1ab42e8a4a67f3445174be5191b'
                conn.sendall(data)
                print(f'[SERVER] File {filename} sent.')

        print(f"[CLOSING CONNECTION] {addr} closed.")
        conn.close()


if __name__ == '__main__':
    main()

