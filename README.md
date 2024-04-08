# Socket Programming: Number Exchange

## Overview
This project demonstrates a simple client-server communication protocol using TCP (Transmission Control Protocol). The main functionality revolves around the exchange of prime numbers between a client and a server, calculation of the Lowest Common Multiple (LCM), and appropriate acknowledgment based on the outcome.

## Protocol Description
The communication protocol is outlined as follows:
1. **Client Initialization**: The client initiates communication with a `100 Hello` message to the server.
2. **Server Acknowledgment**: Upon receiving the “Hello” message, the server responds with `101 Hello Ack`.
3. **Prime Number Exchange**: The client sends `105 Primes a b`, where `a` and `b` are prime numbers.
4. **LCM Calculation**: The server calculates the LCM of `a` and `b`, responding with `107 LCM l`, where `l` is the calculated LCM.
5. **Verification and Response**:
   - If the LCM calculated by the client matches the server’s LCM, the client sends `200 OK`;
   - Otherwise, it sends `400 Error`.

### Error Handling
- **Invalid Prime Numbers**: The server responds with `400 Error` if non-prime numbers are sent.
- **Unexpected Message**: If the client sends an unexpected message, the server responds with `500 Bad Request`.

## Testing Scenarios
Testing was conducted to ensure robust error handling and proper communication flow. The scenarios included:
1. **Valid Scenario**: Client sends valid prime numbers, and the server calculates the correct LCM. The client responds with `200 OK`.
2. **Invalid Prime Numbers**: Client sends non-prime numbers, and the server responds with `400 Error`.
3. **Unexpected Message**: Client sends an unexpected message, prompting a `500 Bad Request` response from the server.

### Expected Outcomes
- **Valid Inputs**: Should result in `200 OK` and the server printing the calculated LCM.
- **Invalid Inputs**: Should lead to `400 Error`.
- **Unexpected Messages**: Should trigger `500 Bad Request`.

## How to Run
1. Start the server by running `server.py`.
2. In a separate terminal, run `client.py` to start the client.
3. Follow the on-screen instructions to initiate the protocol.

## Dependencies
- Python 3
- No external libraries are required for the basic operation of this project.

## Contributors
- Brandon Bradshaw
- 
## License
This project is open source and available under the [MIT License](LICENSE).

