# 1. Python-Postgresql-CloudFoundry
Script em Python para conectar com o Postgresql (do CloudFoundry) para leitura e escrita de dados no Insights Hub(opcional).
## 1.1 - Introdução

Este projeto foi desenvolvido para facilitar a integração entre a plataforma MindSphere (aka Insights Hub) e um banco de dados PostgreSQL, permitindo uma coleta de dados eficiente e automatizada. É ideal para usuários que precisam de uma solução robusta para gerenciamento de dados de IoT.

## 1.2 - Funcionalidades

- Extração automática de dados da API do MindSphere.
- Armazenamento de dados em um banco de dados PostgreSQL.
- Agendamento de tarefas para automação de processos.
- Configuração flexível para diferentes ambientes de execução.

## 1.3 - Tecnologias Utilizadas

- Python
- PostgreSQL
- APScheduler
- CloudFoundry
---
## 2. Instalação

### 2.1 - Pré-requisitos

- Python 3.6 ou superior;
- Acesso ao CloudFoundry;
- Acesso ao Insights Hub (opcional)

### 2.2 - Instalação

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry.git
cd Python-Postgresql-CloudFoundry
```
---
## 3 - Configurações do CloudFoundry
Para configurar todo o CloudFoundry, não é tçao complexo, mas requer atenção:
### 3.1 - Instanciando o PostgreSQL
Você primeiro precisa entender quais pacotes têm na sua Org, para isso, use o seguinte comando:
```bash
cf marketplace
```
<img width="810" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/08eda590-32a2-4a12-9f64-7cd57df305ca">

De acordo com o `offering`, `plans` iremos decidir qual o offering (Postgresql) e o plano fica a seu critério.
Após decidir qual o `plan` irá ser usado, vamos criar a instancia:
```bash
cf create-service <service_orffering> <service_plan> <service_name>
```

Após a criação do `service`, vamos verificar se deu certo a criação:
```bash
cf services
```
<img width="848" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/114c91f4-5bfa-4559-9f43-dfa14accfb0f">

Agora, vá na pasta da sua aplicação que você copiou do Repositório, e copie o caminho e use o `cd`, para trocar o caminho da pasta. Agora, use o `cf push`:
```bash
cf push
```
A sua aplicação constará erro, pois não linkamos o `banco de dados` nem as credenciais. O motivo de darmos o `push`, é para termos nosso app no CloudFoundry e depois linkarmos ele com o PostgreSQL.
### 3.2 - Bind da aplicação
Agora, nós iremos `bindar` a aplicação com o PostgreSQL.
```bash
cf bind-service <app_name> <service_name>
```
<img width="696" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/fd27cba1-cf71-4483-af82-458582b73ad1">

### 3.3 - Credenciais PostgreSQL

Quando a `bind` for feita, agora iremos adquirir os dados de credenciais do PostgreSQL, com o seguinte comando:
```bash
cf env <app_name>
```
<img width="634" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/6619695f-73c6-43e2-bc78-3e51274230d6">

Edite de acordo com as suas credenciais. Abra o arquivo `main.py` para editar as opções nessaa seguinte parte do código:
```python
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="<database_name>",
            user="<database_username>",
            password="<database_password",
            host="<database_host>"
        )
        print('conectado')
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
```

### 3.4 - Funções relacionadas ao PostgreSQL
Abaixo, iremos mostrar algumas funções que podem ser usadas e EDITADAS para o seu caso:
### CRIAR TABELA
```python
#criando a tabela (caso não exista ainda)
def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS <table_name> (
                id SERIAL PRIMARY KEY,
                variavel TEXT NOT NULL,
                valor INTEGER NOT NULL,
                timestamp TEXT NOT NULL);
            """);
        conn.commit()
        print('tabela criada')
        cur.close()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
```

### EDITAR TABELA
```python
#editando a tabela
def edit_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            ALTER TABLE <table_name>
            ADD timestamp VARCHAR(30)
        """)
        conn.commit()
        cur.close()
        print('tabela editada')
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
```

### LIMPAR TABELA
```python
#zerar a tabela
def delete_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM <table_name>;
        """)
        conn.commit()
        cur.close()
        print('tabela zerada')
    except Exception as e:
        print(f"Erro ao zerar tabela: {e}")
```

### INSERIR DADOS
```python
#inserir dados manual
def insert_data(conn, nome, valor):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO <table_name> (variavel, valor) VALUES (%s, %s)", (nome, valor))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
```

### INSERIR DADOS (INSIGHTS HUB - OPCIONAL)
```python
#inserção com timeseries Insights Hub
def insert_timeseries(conn, data):
    try:
        cur = conn.cursor()
        for item in data:
            timestamp = datetime.fromisoformat(item['_time'].rstrip('Z'))
            for key, value in item.items():
                if key != '_time':
                    cur.execute("INSERT INTO <table_name> (variavel, valor, timestamp) VALUES (%s, %s, %s)", (key, value, timestamp))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback()
```

### LEITURA DA TABELA
```python
def read_data(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM <table_name>")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
```
---
## 4. Configuração Insights Hub (OPCIONAL)
Caso você queira fazer essa função utilizando o Insights Hub também, pode continuar o tutorial, mas caso não, pule para o próximo passo ``
*(TUTORIAL EM ANDAMENTO)*
Como não há tutorial ainda, o arquivo `config.py` serve apenas para as APIs do Insights Hub.

## 5. Como usar
- No arquivo `Procfile` é onde está indicado qual arquivo será usado para inicializar, no nosso caso o `main.py`;
- A variavel `data2`, é responsável para armazenar os dados a `API GET` do Insights Hub. Troque esse endpoint caso queira;
- A função `insert_timeseries`, serve para inserir dados requisitados do Insights Hub para o Postgresql (dados já tratados);
- A função `scheduled_task`, serve para as tarefas de agendamento, ou seja, para o nosso caso, ele é usado para executar a tarefa de: `ler dados do Insights Hub > Conectar no PostgreSQL > Inserir dados na Tabela > Retornar esses dados da tabela`

### Caso queira rodar apenas na primeira para criar a tabela, rode a última `main`, e habilite as funções: `create_table(conn)`, `insert_timeseries(conn, data2)`, `read_data(conn)`, `conn.close()`. E então, dê o
```bash
cf push
```

```python
if __name__ == "__main__":
    conn = connect_to_db()
    create_table(conn)
    #delete_table(conn)
    insert_timeseries(conn, data2)
    read_data(conn)
    conn.close()
```

- Para verificar se está tudo certo, rode o seguinte comando:

```
cf logs <app_name> --recent
```

<img width="560" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/e1de48e2-d841-47bf-af98-10dfff69a340">

### Agora, para de fato fazer ela funcionar, habilite o `main` que contem o Agendador
- Na função `scheduled_task`, a gente pode editar o momento em que ela será executada:
```python
if __name__ == "__main__":
    conn = connect_to_db()
    if conn is not None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduled_task, 'interval', minutes=3)  # Executa a cada 3 minutos
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
```
- E use o `cf push`
- Ao ver que o app, foi publicado, verifique usando o `cf apps`:
<img width="559" alt="image" src="https://github.com/Abyss-Whisper/Python-Postgresql-CloudFoundry/assets/61059576/2fd5e9f6-0d99-40c2-b9d6-287770a7bd93">
