import requests
import psycopg2
from config import MindSphere

mindsphere = MindSphere(app_Name="cardapiodigita20",
                        app_Version="v1.0.0",
                        tenant="debr2",
                        gateway_URL="https://gateway.eu1.mindsphere.io/" ,
                        client_ID="debr2-cardapiodigita20-v1.0.0",
                        client_Secret="KhMlcZVzS8YlfvfuCPDSdENRCEE6gvSaFTadq90kVZ9"
                        )

assetId = "31fd2a70282b44dfa2e27c3b1fc6c4eb" #insira aqui o assetID do seu asset
aspectName = "varPython" #insira aqui o aspectName do seu asset
fromDateTime = "2023-07-19T00:00:00Z" #de
toDateTime = "2023-10-16T10:00:00Z"#até


# Funções de conexão com o banco de dados (como no connector.py)

def read_from_endpoint(endpoint_url):
    response = requests.get(endpoint_url)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        return None  # ou lidar com o erro de outra forma
# Ajuste de acordo com o formato da resposta

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
    endpoint_url = mindsphere.getTimeSeries(assetId,aspectName,"","")
    another_endpoint_url = "https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/31fd2a70282b44dfa2e27c3b1fc6c4eb/varPython"

    data = read_from_endpoint(endpoint_url)
    #conn = getDatabaseConnection()
    #store_in_database(conn, data)
    #data = read_from_database(conn)
    #send_to_another_endpoint(another_endpoint_url, data)
    #conn.close()
