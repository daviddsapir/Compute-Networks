#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(cmd: str):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    commands_list = ['TAKE_SCREENSHOT',
                     'SEND_PHOTO',
                     'DIR',
                     'DELETE',
                     'COPY',
                     'EXECUTE',
                     'EXIT']

    cmd = cmd.split(' ')
    command = cmd[0]

    if command not in commands_list:
        return False
    elif command == 'TAKE_SCREENSHOT' and len(cmd) != 1:
        return False
    elif (command == 'DIR' or command == 'DELETE' or command == 'EXECUTE' or command == 'SEND_PHOTO') and len(cmd) != 2:
        return False
    elif command == 'COPY' and len(cmd) != 3:
        return False

    return True


def create_msg(msg):
    """
    Create a valid protocol message, with length field
    """

    return f'{str(len(msg)).zfill(LENGTH_FIELD_SIZE)}{msg}'.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length_field = my_socket.recv(LENGTH_FIELD_SIZE).decode()

    if str(length_field).isnumeric():
        message = my_socket.recv(int(length_field)).decode()
        return True, message
    else:
        return False, "Error"