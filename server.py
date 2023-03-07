import socket
import csv
import sqlite3



#Constants
PORT="port_number"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


# function to manage the client
def client_handler(client_socket):
    # connecting to the SQLite database
    conn = sqlite3.connect('crypto.db')
    cursor = conn.cursor()

    # creating a table for cryptocurrency prices
    cursor.execute("CREATE TABLE IF NOT EXISTS prices (name TEXT NOT NULL PRIMARY KEY, price REAL NOT NULL, date DATE NOT NULL)")

    # adding cryptocurrency prices and other properties to the table in the database
    crypto_prices = [('Bitcoin', 22000.0, '2023-03-01'), ('Ethereum', 1000.0, '2023-03-01'), ('USDCoin', 81.0, '2023-03-01')]
    cursor.executemany("INSERT OR IGNORE INTO prices (name, price, date) VALUES (?, ?, ?)", crypto_prices)

    # committing the changes
    conn.commit()

    # retrieving data
    cursor.execute('SELECT * FROM prices')

    # fetch all rows
    rows = cursor.fetchall()

    #procedures of creating the csv file
    output_file = 'output.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    with open(output_file, "rb") as f:
        csv_data = f.read()

    # sending the CSV data to the client
    client_socket.send(csv_data)
    conn.close()

def start_server():
    # creating a socket object
    server_socket = socket.socket()
    # binding the socket ADDR
    server_socket.bind(ADDR)
    # listen for incoming connections
    server_socket.listen(5)

    while True:
        # accepting connections from outside
        (client_socket, address) = server_socket.accept()
        print(f"Connection from {address} has been initiated!")

        # managing the client connection by calling the client_handler function
        client_handler(client_socket)

        # closing the connection
        client_socket.close()
        break

    # closing the server socket
    server_socket.close()

# starting the server
start_server()

