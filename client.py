import argparse
import asyncio
import os
import shutil
import socket
import time
from threading import Thread

TOTAL_FILES = 160
PORT = 4455
SIZE = 20000000
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"
DIR = 'client_files'

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

ADDR_A = (args.IP_A, PORT)
ADDR_B = (args.IP_B, PORT)


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


async def connect_to_server(server_address):
    reader, writer = await asyncio.open_connection(server_address[0], server_address[1], limit=SIZE)
    print(f'Connected to {server_address}')
    # connect to the servers and return the corresponding StreamWriter and StreamReader
    return reader, writer


async def get_file(filename, reader, writer):
    # send the filename we want to retrieve to the server
    writer.write(filename.encode(FORMAT))
    await writer.drain()
    print('Saving', filename)
    # go to the /client_files directory
    file_path = os.path.join(DIR, filename)
    # save the contents of the retrieved file to an empty one
    with open(file_path, 'wb') as f:
        data = await reader.readuntil(separator=b'EOF')
        data = data.replace(b'EOF', b'')
        f.write(data)

async def main():
    filesA, filesB = get_file_names()
    serverA_address = ADDR_A
    serverB_address = ADDR_B
    # connect to the two servers concurrently
    results = await asyncio.gather(
        connect_to_server(serverA_address),
        connect_to_server(serverB_address)
    )
    # save the expected files
    for fA, fB in zip(filesA, filesB):
        await asyncio.gather(
            get_file(fA, results[0][0], results[0][1]),
            get_file(fB, results[1][0], results[1][1])
        )


if __name__ == "__main__":
    # make sure directory is empty
    if os.path.exists(DIR):
        shutil.rmtree(DIR)
    os.makedirs(DIR)
    # start timer
    t = time.perf_counter()

    # start main()
    asyncio.run(main())

    # stop timer
    elapsed = time.perf_counter() - t
    print(f'Time elapsed since request was sent: {elapsed}')

