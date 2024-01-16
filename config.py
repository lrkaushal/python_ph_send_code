import mysql.connector

# Replace these values with your own database credentials
database_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'db5',
}

# Establish a connection
try:
    connection = mysql.connector.connect(**database_config)
    if connection.is_connected():
        print('Connected to the MySQL database')

    # Perform database operations here

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the connection in the end, whether successful or not
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print('Connection closed')
