#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol
import re

# IP adder to connect to.
IP = '127.0.0.1'

# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = './client_photos' 


def print_instructions():
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')


def get_client_request():
    request = re.sub(' +', ' ', input("Please enter command: "))
    cmd = request.split(' ')[0].upper()
    cmd += ' ' + ''.join(request.split(' ')[1:])

    return cmd.strip()


def handle_server_response(my_socket, cmd: str):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    valid_message, server_response = protocol.get_msg(my_socket)
    cmd = cmd.split(' ')[0]
    if cmd == 'DIR' or cmd == 'DELETE' or cmd == 'COPY':
        print(server_response)


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol.PORT))

    print_instructions()

    # loop until user requested to exit
    while True:
        cmd = get_client_request()
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            if cmd == 'EXIT':
                break
            handle_server_response(my_socket, cmd)
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()