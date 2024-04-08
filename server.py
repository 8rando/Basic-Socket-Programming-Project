# This is the server.py

import socket
import sys
import math

def clientHello():
    """Generates an acknowledgment for the client hello message"""
    msg = "101 Hello Ack"
    return msg

def generateLCMstring(lcm):
    """Generates the 107 LCM string with the calculated LCM value"""
    msg = f"107 LCM {lcm}"  # Include the calculated LCM value in the message
    return msg

def calculateLCM(a, b):
    # Calculate the LCM using the math module
    lcm = math.lcm(a, b)
    return lcm

def processMsgs(s, msg, state):
    """This function processes messages that are read through the socket. It returns
       a status, which is an integer indicating whether the operation was successful."""
    if msg == "100 Hello":
        # Send acknowledgment for client hello
        s.send(clientHello().encode())
        return 101  # Successful

    elif msg.startswith("105 Primes"):
        a, b = map(int, msg.split()[2:])

        if 1031 <= a <= 6397 and 1031 <= b <= 6397:
            # Prime numbers are within the allowed range, calculate LCM
            lcm = calculateLCM(a, b)
            # Send LCM message to the client
            s.send(generateLCMstring(lcm).encode())
            # Receive the client's response
            client_response = s.recv(1024).decode()

            if client_response == "200 OK":
                print(f"Client's response: 200 OK (LCM: {lcm})")
                return 200  # Successful
            elif client_response == "400 Error":
                print("Client's response: 400 Error")
                return 400  # Error
            else:
                print("500 Bad Request")
                return 500  # Bad Request
        else:
            # Prime numbers are out of the allowed range
            print("Prime numbers are out of the allowed range (1031-6397)")
            s.send("400 Error".encode())  # Send an error response
            return 400  # Error
    else:
        print("500 Bad Request")
        return 500  # Bad Request

def main():
    """Driver function for the server."""
    args = sys.argv
    if len(args) != 2:
        print("Please supply a server port.")
        sys.exit()
    HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
    PORT = 55555  # The port on which the server is listening.
    if (PORT < 1023 or PORT > 65535):
        print("Invalid port specified.")
        sys.exit()

    client_name = str(input("Enter your name: "))
    print(f"Server of {client_name}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket
        s.bind((HOST, PORT))
        # listen
        s.listen(1)
        conn, addr = s.accept()  # accept connections using socket
        with conn:
            print("Connected from: ", addr)

            while True:
                data = conn.recv(1024).decode()

                if not data:
                    break  # Connection closed

                print("Received: ", data)

                status = processMsgs(conn, data, {})  # Pass an empty state dictionary

            conn.close()
            print("Connection closed")

if __name__ == "__main__":
    main()
