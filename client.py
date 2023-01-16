import argparse
import asyncio
import os
import socket
import time
from threading import Thread

TOTAL_FILES = 160
PORT = 4455
SIZE = 20000000
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"

parser = argparse.ArgumentParser(
    prog='TCP multiple file transfer client',
    description='Requests multiple files from two servers,' + 
        'with a customizable ratio of downloaded files from each server.'
)

parser.add_argument('n_A', help='Number of files to get from server A (in one request)', type=int)
parser.add_argument('n_B', help='Number of files to get from server B (in one request)', type=int)
parser.add_argument('IP_A', help='IP address of server A')
parser.add_argument('IP_B', help='IP address of server B')

args = parser.parse_args()

async def download_file(writer, reader, file_name):
    print('Requesting', file_name)
    request = f'{file_name}'.encode()
    writer.write(request)  # Request file
    await writer.drain()
    response = await reader.read()
    writer.close()
    return response

def save_file(response, file_name):
    print('Saving', file_name)
    directory = 'client_files'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as f:
        f.write(response)
    print(f'File {file_name} saved.')

def get_file_names():
    filesA = []
    filesB = []
    step = args.n_A + args.n_B
    for i in range(1, 161, step):
        for a in range(i, i+args.n_A):
            if (a <= 160):
                file_name = f's{str(a).zfill(3)}.m4s'
                filesA.append(file_name)

    for i in range(1+args.n_A, 161, step):
        for b in range(i, i+args.n_B):
            if (b <= 160):
                file_name = f's{str(b).zfill(3)}.m4s'
                filesB.append(file_name)

    return filesA, filesB

async def faultymain():
    filesA, filesB = get_file_names()
    readerA, writerA = await asyncio.open_connection(args.IP_A, PORT)
    # readerB, writerB = await asyncio.open_connection(args.IP_B, PORT)
    tasksA = [asyncio.ensure_future(download_file(writerA, readerA, file_nameA)) for file_nameA in filesA]
    # tasksB = [asyncio.create_task(download_file(writerB, readerB, file_nameB)) for file_nameB in filesB]
    
    tasks = tasksA #+ tasksB
    s = time.perf_counter()
    responses = await asyncio.gather(*tasks)
    print('Respones gathered. Start saving...')
    for response, file_name in zip(responses, filesA): # + filesB
        await save_file(response, file_name)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    writerA.close()
    # writerB.close()

def main(IP, files):
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the Servers
    print(f'Connecting to {IP} port {PORT}')
    s.connect((IP, PORT))

    # Send the file name to Servers
    for file in files:
        print('File a:', file)
        s.sendall(file.encode(FORMAT))

        # Receive the file
        print('receiving data a')
        while True:
            data = s.recv(SIZE)
            if not data:
                print('Finished')
                break
            save_file(data, file)
            print('--file received a--')
            break
    s.close()


if __name__ == "__main__":
    filesA, filesB = get_file_names()
    threads = []
    # create threads
    threads.append(Thread(target=main(args.IP_A, filesA)))
    threads.append(Thread(target=main(args.IP_B, filesB)))
    # start timer
    t = time.perf_counter()
    # start threads
    for thread in threads:
        thread.start() 
    # end threads (?)
    for thread in threads:
        thread.join()
    # stop timer
    elapsed = time.perf_counter() - t
    print(f'Time elapsed since request was sent: {elapsed}')




