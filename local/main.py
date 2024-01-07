import psycopg2
import datetime

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
        #insert_data(conn, "var1", 100, today)
        #insert_data(conn, "var2", 150, today)#
        read_data(conn)
        conn.close()
