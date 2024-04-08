import socket
import sys
import math

def serverHello():
    """Generates server hello message"""
    status = "100 Hello"
    return status

def AllGood():
    """Generates 200 OK"""
    status = "200 OK"
    return status

def ErrorCondition():
    """Generates 400 Error"""
    status = "400 Error"
    return status

def PrimeCollect():
    primeNbr = input("Enter a prime number between 1031 and 6397: ")
    return primeNbr

def PrimeMsg(prime1, prime2):
    msg = f"105 Primes {prime1} {prime2}"
    return msg

def processMsgs(s, msg, state):
    if msg == "101 Hello Ack":
        try:
            # Prompt the client for two prime numbers
            prime1 = int(PrimeCollect())
            prime2 = int(PrimeCollect())

            if not (1031 <= prime1 <= 6397 and 1031 <= prime2 <= 6397 and is_prime(prime1) and is_prime(prime2)):
                # Send "400 Error" for out-of-range prime numbers
                s.send(ErrorCondition().encode())
                return 400

            # Send "105 Primes" message to the server with the two valid prime numbers
            s.send(PrimeMsg(prime1, prime2).encode())

            # Receive the server's response
            lcm_message = s.recv(1024).decode()

            if lcm_message.startswith("107 LCM"):
                # Extract LCM value from the message
                lcm = int(lcm_message.split()[2])

                if lcm == math.lcm(prime1, prime2):
                    # Send "200 OK" if LCM is correct
                    s.send(AllGood().encode())
                    return 200
                else:
                    # Send "400 Error" if LCM is incorrect
                    s.send(ErrorCondition().encode())
                    return 400
            else:
                # Handle unexpected server response
                print("Unexpected server response")
                return 500
        except ValueError:
            # Handle the case where the user input cannot be converted to integers
            print("Unexpected bad response")
            s.send("Unexpected bad response".encode())
            return 500
    else:
        # Handle unexpected message from the server
        s.send("Unexpected server response".encode())
        return 500

    

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    args = sys.argv
    if len(args) != 3:
        print("Please supply a server address and port.")
        sys.exit()

    serverHost = '127.0.0.1'  # The remote host
    serverPort = int(55555)  # The port used by the server

    client_name = str(input("Enter your name: "))
    print(f"Client of {client_name}")
    print("""
    The purpose of this program is to collect two prime numbers from the client, and then
    send them to the server. The server will compute their LCM and send it back to the
    client. If the server-computed LCM matches the locally computed LCM, the client sends
    the server a 200 OK status code. Otherwise, it sends a 400 Error status code, and
    then closes the socket to the server.
    """)

    server_address = (serverHost, serverPort)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        serverHost = '127.0.0.1'  # The remote host
        serverPort = 55555  # The port used by the server
        s.connect((serverHost, serverPort))
        print(f"Connected to the server at {serverHost}:{serverPort}")

        msg = serverHello()
        s.send(msg.encode())

        data = s.recv(1024).decode()
        print(f"Received: {data}")

        status = processMsgs(s, data, {})

        if status == 200:
            print("Server response: 200 OK")
        elif status == 400:
            print("Server response: 400 Error")
        elif status == 500:
            print("Server response: 500 Bad Request")

        s.close()
        print("Connection to the server closed")

if __name__ == "__main__":
    main()
