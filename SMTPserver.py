import socket

def handle_client_connection(client_socket):
    valid_commands = ["HELO", "MAIL", "RCPT", "DATA", "QUIT"]
    current_state = 0  # Represents the current state in the command sequence

    client_socket.send(b"220 Welcome to My SMTP Server\r\n")

    while True:
        try:
            data = client_socket.recv(1024).decode().strip()

            if not data:
                break

            print("Received:", data)

            if data not in valid_commands:
                client_socket.send(b"503 Bad sequence of commands\r\n")
                break

            if data == "QUIT":
                client_socket.send(b"221 Goodbye\r\n")
                break
            elif data == "HELO" and current_state == 0:
                client_socket.send(b"250 OK\r\n")
                current_state = 1
            elif data == "MAIL" and current_state == 1:
                client_socket.send(b"250 OK\r\n")
                current_state = 2
            elif data == "RCPT" and current_state == 2:
                client_socket.send(b"250 OK\r\n")
                # RCPT can be accepted multiple times, so stay in the same state
            elif data == "DATA" and current_state == 2:
                client_socket.send(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                current_state = 3
            elif data == "." and current_state == 3:
                client_socket.send(b"250 OK\r\n")
                current_state = 2  # Reset state after successfully receiving data
            else:
                client_socket.send(b"503 Bad sequence of commands\r\n")

        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

def start_smtp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.179.1", 25)  # Use port 25 for SMTP
    server_socket.bind(server_address)
    server_socket.listen(1)

    print('SMTP server is listening on {}:{}'.format(*server_address))

    while True:
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from', client_address)

        handle_client_connection(client_socket)

if __name__ == "__main__":
    start_smtp_server()
