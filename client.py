import socket

#constants
PORT="port_number"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# creating a socket object for the client side
client_socket = socket.socket()

# connecting to the server to ADDR
client_socket.connect(ADDR)
# receiving the CSV data from the server
csv_data = client_socket.recv(1024)

# saving the CSV data to a file
with open("data.csv", "wb") as f:
    f.write(csv_data)

client_socket.close()
