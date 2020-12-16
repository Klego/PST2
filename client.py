from protocols_messages import *
# import utils
import socket
from inputcontrol import *


def manage_welcome(c_socket, players, stages):
    print(msg_client["Message"])
    send_option = ""
    while send_option not in msg_client["Option_Range"]:
        send_option = input("\nYour option: ")
        if send_option not in msg_client["Option_Range"]:
            print("Option must be between 1 and 3. Try again")
    reply_welcome = craft_send_server_option(send_option, players, stages)
    c_socket.sendall(reply_welcome)


def manage_choose_character(c_socket):
    print(msg_client["Message"])
    choose_character = ""
    while choose_character not in msg_client["Options_Range"]:
        choose_character = input("Choose one option: ")
        if choose_character not in msg_client["Options_Range"]:
            print("The characters options are between 1 and 4. Try again")
    send_character = craft_send_character(choose_character)
    c_socket.sendall(send_character)


def manage_msgserver():
    print(msg_client["Message"])

#     depende del mensaje


def manage_turn(c_socket):
    print(msg_client["Message"])
    command = ""
    while command not in msg_client["Range_Options"]:
        command = input("Choose one option: ")
        if command not in msg_client["Range_Options"]:
            print("Option not valid. Try again")
    send_command = craft_send_character_command(command)
    c_socket.sendall(send_command)


def manage_games(c_socket):
    print(msg_client["Message"])
    selected_game = ""
    while selected_game not in msg_client["Options_Range"]:
        selected_game = input("Choose one option: ")
    send_selected = craft_send_game_choice(selected_game)
    c_socket.sendall(send_selected)


def manage_valid_game():
    print(msg_client["Message"])


def manage_endgame():
    if msg_client["Win"]:
        print("All the stages have been cleared. CONGRATS! YOU WON THE GAME!")
    else:
        print("All characters have been defeated. Try again. GAME OVER")


def manage_dcserver():
    print(msg_client["Reason"])


def msg_join(c_socket, nick):
    send_name = craft_join(nick)
    c_socket.sendall(send_name)


try:
    n_players, n_stages, ip, port, name = parse_args_client()
    check_args(n_players, n_stages, name)
    port = check_port(port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    msg_join(client_socket, name)
    finalize = False
    while not finalize:
        msg_type = client_socket.recv(1024)
        msg_client = decoded_msgs(msg_type)
        if msg_client["Protocol"] == PROTOCOL_WELCOME:
            manage_welcome(client_socket, n_players, n_stages)
        elif msg_client["Protocol"] == PROTOCOL_CHOOSE_CHARACTER:
            manage_choose_character(client_socket)
        elif msg_client["Protocol"] == PROTOCOL_SERVER_MSG:
            manage_msgserver()
        elif msg_client["Protocol"] == PROTOCOL_YOUR_TURN:
            manage_turn(client_socket)
        elif msg_client["Protocol"] == PROTOCOL_SEND_GAMES:
            manage_games(client_socket)
        # elif msg_client["Protocol"] == PROTOCOL_SEND_VALID_GAME:
        #     manage_valid_game()
        # elif msg_client["Protocol"] == PROTOCOL_SEND_END_GAME:
        #     manage_endgame()
        #     finalize = True
        elif msg_client["Protocol"] == PROTOCOL_SEND_DC_SERVER:
            manage_dcserver()
            finalize = True
    client_socket.close()
except ConnectionResetError:
    print("The connection to the server has been interrupted")
except ConnectionRefusedError:
    print("Could not connect to the server. Are you sure you have provided the correct ip and port?")
except ArgumentError:
    print("Program finished due to bad arguments.")
except KeyboardInterrupt:
    print("Program finished due to CTRL+C command.")