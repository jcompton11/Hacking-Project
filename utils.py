import socket
import argparse as parse
import string
import itertools
import json


def get_args():
    parser = parse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for socket connection')
    parser.add_argument('port', type=int, help='Port to make a socket connection')
    # parser.add_argument('--message', type=str, help='password message to establish a connection')

    args = parser.parse_args()
    return args.ip, args.port


def connect_to_server(ip_address, port_num):
    address = (ip_address, port_num)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    return client


def send_data(sender_socket, data):
    sender_socket.send(data.encode())


def receive_data(client):
    response = client.recv(1024)
    return response.decode()


# generates passwords starting with a single character
def pass_gen():
    arr = string.ascii_letters + string.digits
    for length in range(1, len(arr)):
        for attempt in itertools.product(arr, repeat=length):
            yield ''.join(attempt)


# this just yields a character along the array given
def pass_gen2():
    arr = string.ascii_letters + string.digits
    for ch in arr:
        yield ch


# modifies passwords by changing cases iteratively using product
def modify_passcode(passcode):
    for p in itertools.product(*zip(passcode.upper(), passcode.lower())):
        yield ''.join(p)


# uses dictionary file of passwords or logins to search for viable entries
def dictionary_gen(file_name):
    with open(file_name, 'r') as f:
        for line in f.readlines():
            for attempt in modify_passcode(line.strip()):
                yield attempt


def login_dictionary_gen(file_name):
    with open(file_name, 'r') as f:
        for line in f.readlines():
            yield line.strip()


# json string sent as data to the server
def json_data(login, password):
    return json.dumps({'login': login, 'password': password}, indent=4)


# json response is decoded into a simple msg
def json_response(json_msg):
    return json.loads(json_msg)
