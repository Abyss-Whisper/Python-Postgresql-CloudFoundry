import psycopg2
from datetime import datetime
from config import MindSphere
import json

mindsphere = MindSphere(app_Name="<YOUR_APP_NAME>", #app_name
                        app_Version="<YOUR_APP_VERSION>", #v1.0.0
                        tenant="<YOUR_APP_TENANT>", #tenant
                        gateway_URL="https://gateway.eu1.mindsphere.io/", #don't edit
                        client_ID="<YOUR_Client_ID>", 
                        client_Secret="YOUR_CLIENT_SECRET"
                        )


assetId = "<YOUR_ASSET_ID>" #insira aqui o assetID do seu asset
aspectName = "<YOUR_ASPECT_NAME>" #insira aqui o aspectName do seu asset
fromDateTime = "" #2024-01-01T00:00:00Z <- examplo
toDateTime = ""#2024-01-01T00:00:00Z <- exemplo

print(mindsphere.getTimeSeries(assetId,aspectName,"","")) #retorna o último timestamp disponível

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="python",
            user="postgres",
            password="admin",
            host="localhost"
        )
        print('conectado')
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

#criando a tabela (caso não exista ainda)

'''def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            ALTER TABLE timeseries
            ADD timestamp VARCHAR(30)
        """)
        conn.commit()
        cur.close()
        print('tabela criada')
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")'''

#inserir dados
'''def insert_data(conn, nome, valor):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO timeseries (variavel, valor) VALUES (%s, %s)", (nome, valor))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")'''

#inserção com timeseries
def insert_timeseries(conn, data):
    try:
        cur = conn.cursor()
        for item in data:
            timestamp = datetime.fromisoformat(item['_time'].rstrip('Z'))
            for key, value in item.items():
                if key != '_time':
                    cur.execute("INSERT INTO timeseries (variavel, valor, timestamp) VALUES (%s, %s, %s)", (key, value, timestamp))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback()

# Exemplo de uso
data = [{'temp': 50, 'velo': 90.0, '_time': '2024-01-07T03:02:03.431Z'}]
data2 = mindsphere.getTimeSeries(assetId,aspectName,"","")
'''conn = connect_to_db()
insert_timeseries(conn, data)
conn.close()'''


#ler dados
def read_data(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM timeseries")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print(f"Erro ao ler dados: {e}")

#execução

if __name__ == "__main__":
    conn = connect_to_db()
    if conn is not None:
        #create_table(conn)
        #insert_data(conn, "var1", 900)
        #insert_data(conn, "var2", 150, today)#
        insert_timeseries(conn, data2)
        read_data(conn)
        conn.close()