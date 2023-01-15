
import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 20000000
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

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        """ Receiving the filename from the client. """
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the filename.")
        print(filename)
        file = open(f"server_data/files/{filename}", "rb")
        conn.sendfile(file)

        """ Closing the file. """
        file.close()

        """ Closing the connection from the server. """
    server.close()


if __name__ == '__main__':
    main()
'''def main():
    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM means we are using a TCP connection
    server.bind(ADDR)
    server.listen()
    print('[LISTENING] Server is listening.')

    while True:
        conn, addr = server.accept()
        print(f'[NEW CONNECTION] {addr} connected.')

        """ Receiving folder name """
        folder_name = conn.recv(SIZE).decode(FORMAT)

        """ Creating the folder """
        folder_path = os.path.join(SERVER_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            conn.send(f'Folder {folder_name} created.'.encode(FORMAT))
        else:
            conn.send(f'Folder {folder_name} already exists.'.encode(FORMAT))

        """ Receiving files """
        while True:
            msg = conn.recv(SIZE).decode(FORMAT)
            cmd, data = msg.split(':')

            if cmd == 'FILENAME':
                """ Recv the file name """
                print(f'[CLIENT] Received the filename: {data}.')

                file_path = os.path.join(folder_path, data)
                file = open(file_path, 'w')
                conn.send('Filename received.'.encode(FORMAT))


if __name__ == '__main__':
    main()'''


'''
  files = sorted(os.listdir(path))
    for i, file_name in enumerate(files):
        """ Sending the file name """
        if i in RM:
            continue
        msg = f'FILENAME:{file_name}'
        print(f'[SERVER] Sending file name: {file_name}.')
        server.send(msg.encode(FORMAT))

        """ Receiving the reply from the server """
        msg = server.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
'''