
import socket
import protocol
import shutil
import os
from glob import glob

# IP adder to connect to.
IP = '127.0.0.1'

# The path + filename where the screenshot at the server should be saved
PHOTO_PATH = 'server_photos'


def check_if_file_exist(path: str):
    return os.path.isfile(path)


def check_if_dir_exist(path: str):
    return os.path.isdir(path)


def check_client_request(request: str):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """

    cmd = ''
    params = list()
    # Use protocol.check_cmd first
    if protocol.check_cmd(request):
        request = request.split(' ')
        cmd = request[0]

        if cmd == 'EXIT':
            params.append(None)
        if cmd == 'DIR':
            if check_if_dir_exist(request[1]):
                params.append(request[1])
            else:
                return False
        if cmd == 'DELETE':
            if check_if_file_exist(request[1]):
                params.append(request[1])
            else:
                return False
        if cmd == 'COPY':
            if check_if_file_exist(request[1]) and\
                    check_if_file_exist(request[2]):
                params.append(request[1])
                params.append(request[2])
            else:
                return False

    # Then make sure the params are valid

    # (6)

    return True, cmd, params


def handle_client_request(command: str, params: list):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data
    
    """

    if command == 'DIR':
        path = params[0]
        if path[-1] != '/':
            path += '/'
        response = '\n'.join(glob(path + '*')) + '\n'
    if command == 'DELETE':
        path = params[0]
        os.remove(path)
        response = 'Removed - ' + path
    if command == 'COPY':
        shutil.copy(params[0], params[1])
        response = f'Copied {params[0]} to {params[1]}'
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))

    # begin listening for clients
    server_socket.listen()
    print('Server is listening for clients')

    # accept a client.
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Checks if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                if command == 'EXIT':
                    break
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)

                # add length field using "create_msg"
                packet = protocol.create_msg(response)

                # send to client
                client_socket.send(packet)

                # if command == 'SEND_FILE':
                #     # Send the data itself to the client
                #
                #     # (9)
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                client_socket.send(response.encode())
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'

            # send to client
            client_socket.send(response.encode())

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
