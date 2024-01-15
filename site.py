import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Interface do Streamlit para inserir dados de compra
produto = st.text_input('Produto:')
qtd_parcelas = st.number_input('Quantidade de Parcelas:', step=1, format="%d")
valor_parcela = st.number_input('Valor da Parcela:', step=0.01, format="%.2f")
data_pagamento = st.date_input('Data de Pagamento:')

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('teste.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT NOT NULL,
        qtd_parcelas INTEGER NOT NULL,
        valor_parcela REAL NOT NULL,
        data_pagamento DATE NOT NULL
    )
''')

# Inserir dados na tabela test_compras
cursor.execute('''
    INSERT INTO test_compras (produto, qtd_parcelas, valor_parcela, data_pagamento)
    VALUES (?, ?, ?, ?)
''', (produto, qtd_parcelas, valor_parcela, data_pagamento))

# Commit para salvar as alterações no banco de dados
conn.commit()

# Consultar dados da tabela test_compras para criar o seletor de produtos
df_compras = pd.read_sql_query('SELECT * FROM test_compras', conn)

# Criar a tabela test_datas se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_datas (
        data_parcela DATE NOT NULL,
        valor_parcela REAL NOT NULL,
        produto TEXT,
        FOREIGN KEY (produto) REFERENCES test_compras(produto)
    )
''')

# Inserir dados na tabela test_datas com base nas informações de compra
for i in range(qtd_parcelas):
    data_parcela = data_pagamento + relativedelta(months=i)
    cursor.execute('''
        INSERT INTO test_datas (data_parcela, valor_parcela, produto)
        VALUES (?, ?, ?)
    ''', (data_parcela, valor_parcela, produto))

# Commit para salvar as alterações no banco de dados
conn.commit()

df_datas = pd.read_sql_query('SELECT * FROM test_datas', conn)

#def criar_dfcompras():
#    cursor.execute('SELECT * FROM test_compras')
#    data = cursor.fetchall()
#    column_names = [description[0] for description in cursor.description]
#    df_compras = pd.DataFrame(data, columns=column_names)
#    return df_compras

#def criar_dfdatas():
#    cursor.execute('SELECT * FROM test_datas')
#    data = cursor.fetchall()
#    column_names = [description[0] for description in cursor.description]
#    df_datas = pd.DataFrame(data, columns=column_names)
#    return df_datas

def tabela():
        st.title('Lançamentos')
        
        #df_compras = criar_dfcompras()
        #df_datas = criar_dfdatas()
        
        # Filtro por múltiplos produtos usando st.sidebar.multiselect
        produtos_selecionados = st.sidebar.multiselect('Escolha os Produtos:', df_compras['produto'].unique())

        # Aplicar filtro nas duas tabelas usando isin
        df_filtrado_compras = df_compras[df_compras['produto'].isin(produtos_selecionados)]
        df_filtrado_datas = df_datas[df_datas['produto'].isin(produtos_selecionados)]

        # Mostrar os DataFrames resultantes
        st.sidebar.subheader('Compras Filtradas')
        st.sidebar.dataframe(df_filtrado_compras)

        st.sidebar.subheader('Datas Filtradas')
        st.sidebar.dataframe(df_filtrado_datas)

# Chamar a função para renderizar na interface
tabela()
        