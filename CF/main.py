import psycopg2
from datetime import datetime
from config import MindSphere
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

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

print(mindsphere.getTimeSeries(assetId,aspectName,"","")) #retorna o último timestamp disponível

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="pod9164fc",
            user="a9s6789382dcc59ed571f89c04d3274cb611f051ac6",
            password="a9sdd5cde722f5f38c623b75cd1d396b71ec49db89e",
            host="pod9164fc-psql-master-alias.node.dc1.a9ssvc"
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
            CREATE TABLE IF NOT EXISTS timeseries (
                id SERIAL PRIMARY KEY,
                variavel TEXT NOT NULL,
                valor INTEGER NOT NULL,
                timestamp TEXT NOT NULL);
            """);
        conn.commit()
        print('tabela criada')
        cur.close()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")'''

#editando a tabela
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

#inserir dados manual
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

data2 = mindsphere.getTimeSeries(assetId,aspectName,"","")

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

def scheduled_task():
    conn = connect_to_db()
    if conn is not None:
        data2 = mindsphere.getTimeSeries(assetId, aspectName, "", "")
        insert_timeseries(conn, data2)
        read_data(conn)
        conn.close()

#inicializar o programa
if __name__ == "__main__":
    conn = connect_to_db()
    if conn is not None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduled_task, 'interval', minutes=1)  # Executa a cada hora
        scheduler.start()

        # Desliga o agendador quando o aplicativo encerrar
        atexit.register(lambda: scheduler.shutdown())

        # Mantém o script em execução
        while True:
            pass
    #create_table(conn)
    insert_timeseries(conn, data2)
    read_data(conn)
    conn.close()