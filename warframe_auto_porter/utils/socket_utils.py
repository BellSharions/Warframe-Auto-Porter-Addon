from ..constants import special_reset_rules
from .helpers import strtobool


def set_default(input_socket, value):
    if input_socket.type == 'VECTOR':
        input_socket.default_value = tuple(value[:3])
    elif input_socket.type == 'BOOLEAN':
        input_socket.default_value = bool(strtobool(value))
    elif input_socket.type == 'COLOR':
        input_socket.default_value = tuple(value[:3])
    elif input_socket.type == 'RGBA':
        input_socket.default_value = tuple(value[:4])
    elif input_socket.type == 'VALUE':
        input_socket.default_value = float(value)
    elif input_socket.type == 'INT':
        input_socket.default_value = int(value)


def reset_default(input_socket):
    socket_name = input_socket.name
    if socket_name in special_reset_rules:
        input_socket.default_value = special_reset_rules[socket_name]
        return
    if input_socket.type == 'VECTOR':
        input_socket.default_value = tuple([0, 0, 0])
    elif input_socket.type == 'BOOLEAN':
        input_socket.default_value = False
    elif input_socket.type == 'COLOR':
        input_socket.default_value = tuple([0.5, 0.5, 0.5])
    elif input_socket.type == 'RGBA':
        input_socket.default_value = tuple([0.5, 0.5, 0.5, 1])
    elif input_socket.type == 'VALUE':
        input_socket.default_value = float(0)
    elif input_socket.type == 'INT':
        input_socket.default_value = int(0)
