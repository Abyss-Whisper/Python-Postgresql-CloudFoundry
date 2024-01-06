import requests
import psycopg2


# Funções de conexão com o banco de dados (como no connector.py)

def read_from_endpoint(endpoint_url):
    response = requests.get(endpoint_url)
    return response.json()  # Ajuste de acordo com o formato da resposta

def store_in_database(conn, data):
    cur = conn.cursor()
    # Substitua com sua consulta SQL para inserir dados
    cur.execute("INSERT INTO sua_tabela (coluna) VALUES (%s)", (data,))
    conn.commit()
    cur.close()

def read_from_database(conn):
    cur = conn.cursor()
    cur.execute("SELECT coluna FROM sua_tabela ORDER BY id DESC LIMIT 1")  # Ajuste sua consulta
    data = cur.fetchone()
    cur.close()
    return data

def send_to_another_endpoint(another_endpoint_url, data):
    requests.post(another_endpoint_url, json=data)  # Ajuste conforme necessário

# Fluxo principal
if __name__ == '__main__':
    endpoint_url = "https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/31fd2a70282b44dfa2e27c3b1fc6c4eb/varPython/temp"
    another_endpoint_url = "https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/31fd2a70282b44dfa2e27c3b1fc6c4eb/varPython"

    data = read_from_endpoint(endpoint_url)
    #conn = getDatabaseConnection()
    #store_in_database(conn, data)
    #data = read_from_database(conn)
    #send_to_another_endpoint(another_endpoint_url, data)
    #conn.close()
