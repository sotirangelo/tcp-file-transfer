import argparse
import asyncio
import os
import shutil
import time

TOTAL_FILES = 160
PORT = 4455
SIZE = 20000000
FORMAT = "utf"
DIR = 'client_data'

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
    """
    * Function that given the file ratio for each server returns the file names each one needs to send.
    * Ex.: client.py n_A=2 n_B=1 IP_A IP_B, server with IP_A is going to send files s001.m4s, s002.m4s, s004.m4s
    * and server with IP_B is going to send files s003.m4s, s006.m4s etc.
    @return: [] filesA containing the filenames for server with IP_A, [] filesB containing the filenames
    for server with IP_B to send
    """
    filesA = []
    filesB = []
    step = args.n_A + args.n_B
    for i in range(1, 161, step):
        for a in range(i, i + args.n_A):
            if a <= 160:
                file_name = f's{str(a).zfill(3)}.m4s'
                filesA.append(file_name)

    for i in range(1 + args.n_A, 161, step):
        for b in range(i, i + args.n_B):
            if b <= 160:
                file_name = f's{str(b).zfill(3)}.m4s'
                filesB.append(file_name)

    return filesA, filesB


async def connect_to_server(server_address):
    """
    * Function that given a server address tuple initiates a connection and returns the appropriate
    * StreamReader reader and StreamWriter writer.
    @param (ADDR, PORT) specifying the address of the server we want to connect.
    @return: StreamReader reader object, StreamWriter writer object
    """
    reader, writer = await asyncio.open_connection(server_address[0], server_address[1], limit=SIZE)
    print(f'[NEW CONNECTION] Connected to server {server_address}.')
    return reader, writer


async def get_file(filename, reader, writer):
    """
    * Function that sends the server the filename we want to download and writes the response in a file with
    * the same name inside directory DIR = 'client_data'.
    @param filename: str name of file we want to download
    @param reader: StreamReader object to read file from server
    @param writer: StreamWriter object to write server the filename we want to receive
    """
    """ Send the filename we want to retrieve to the server """
    writer.write(filename.encode(FORMAT))
    await writer.drain()
    print(f'[CLIENT] Saving file: {filename}')
    file_path = os.path.join(DIR, filename)
    """ Save the contents of the retrieved file to an empty one """
    with open(file_path, 'wb') as f:
        data = await reader.readuntil(separator=b'EOF')
        data = data.replace(b'EOF', b'')
        f.write(data)


async def main():
    """
    * Main function that initiates connection to the two servers and calls get_file() for each file
    * in corresponding list.
    """
    filesA, filesB = get_file_names()
    serverA_address = ADDR_A
    serverB_address = ADDR_B
    """ Connect to the two servers concurrently """
    results = await asyncio.gather(
        connect_to_server(serverA_address),
        connect_to_server(serverB_address)
    )
    """ Save the expected files """
    for fA, fB in zip(filesA, filesB):
        await asyncio.gather(
            get_file(fA, results[0][0], results[0][1]),
            get_file(fB, results[1][0], results[1][1])
        )


if __name__ == "__main__":
    """ Make sure directory is empty """
    if os.path.exists(DIR):
        shutil.rmtree(DIR)
    os.makedirs(DIR)
    """ Start timer """
    t = time.perf_counter()

    """ Start main() """
    asyncio.run(main())

    """ Stop timer """
    elapsed = time.perf_counter() - t
    print(f'[TIME] Time elapsed since request was sent: {elapsed}')
