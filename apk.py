import streamlit as st
import pandas as pd
import sqlite3
import random
import string

conn = sqlite3.connect('dados_compras.db')
cursor = conn.cursor()

def registrar_produto():
    cursor.execute('CREATE TABLE IF NOT EXISTS novos_produtos (id_produto TEXT PRIMARY KEY, produto TEXT NOT NULL, modelo TEXT NOT NULL, tamanho TEXT NOT NULL)')
    conn.commit()

def registrar_compra():
    cursor.execute('CREATE TABLE IF NOT EXISTS compras (id_produto TEXT PRIMARY KEY, segmento TEXT NOT NULL, produto TEXT NOT NULL, modelo TEXT NOT NULL, tamanho TEXT NOT NULL, genero TEXT NOT NULL, publico TEXT NOT NULL, quantidade INTEGER NOT NULL, data_compra DATE NOT NULL, preco REAL NOT NULL, custos_adicionais REAL NOT NULL, pagamento TEXT NOT NULL, forma_de_pagamento TEXT NOT NULL, parcelas INTEGER NOT NULL, valor_entrada REAL NOT NULL, valor_parcela REAL NOT NULL, data_pagamento DATE NOT NULL, fornecedor TEXT NOT NULL, data_entrega DATE NOT NULL, preco_unitario REAL NOT NULL, preco_final REAL NOT NULL)')
    conn.commit()

def inserir_dados(id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final):
    if produto == 'Novo Produto':
        cursor.execute('INSERT INTO novos_produtos (id_produto, produto, modelo, tamanho) VALUES (?, ?, ?, ?)', (id_produto, produto, modelo, tamanho))
    cursor.execute('INSERT INTO compras (id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcelas, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final))

def acesso():
    codigo_de_acesso = st.text_input('Código de Acesso', type='password')
    entrar = st.button('Entrar')
    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
        st.experimental_rerun()
    elif entrar:
        st.warning("O código de acesso inserido não foi aceito, tente novamente.")

def gerar_id_unico():
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=5))
    return letras + numeros

def coleta():
    id_produto = gerar_id_unico()
    
    opcao_produtos = ['Novo produto']
    
    cursor.execute('SELECT produto FROM novos_produtos')
    produtos_existentes = cursor.fetchall()
    
    def custom_sort_key(a1):
            return a1 if a1 != 'Novo Produto' else 'zzz'
    
    opcao_produtos.extend(sorted([item[0] for item in produtos_existentes], key=custom_sort_key))
    
    produto = st.selectbox('Produto Comprado', opcao_produtos)
        
    if produto == 'Novo Produto':
        novo_produto = st.text_input('Novo Produto')
    
        if novo_produto:
            cursor.execute('INSERT INTO novos_produtos (produto) VALUES (?)', (novo_produto,))
            conn.commit()
        
    if produto == 'Novo Produto':
        novo_produto = st.text_input('Novo Produto')
    
    opcao_modelo = ['Novo Modelo'] 
    
    def custom_sort_key(a2):
            return a2 if a2 != 'Novo Modelo' else 'zzz'
    modelo_ordenados = sorted(opcao_modelo, key=custom_sort_key)
    modelo = st.selectbox('Modelo Comprado', modelo_ordenados)

    if modelo == 'Novo Modelo':
        novo_modelo = st.text_input('Novo Modelo')
        if novo_modelo:
            cursor.execute('INSERT INTO novos_produtos (modelo) VALUES (?)', (novo_modelo,))
            conn.commit()

    nicho = ['Masculino', 'Feminino', 'Unissex']
    genero = st.selectbox('Gênero', nicho)
    faixa = ['Adulto', 'Infantil']
    publico = st.selectbox('Público', faixa)
    quantidade = st.number_input("Quantidade Comprada", step=1, format="%d")
    data_compra = st.date_input('Data da Compra')
    preco = st.number_input('Preço da Compra em Reais', step=0.01, format="%.2f")
    custos_adicionais = st.number_input('Custos Adicionais', step=0.01, format="%.2f")
    paga = ['À Vista', 'Parcelamento']
    pagamento = st.selectbox("Forma de Pagamento", paga)
    opcoes_pagamento = ["Boleto Bancário", "PIX", "Dinheiro Vivo", "Cartão de Crédito", "Cartão de Débito"]
    forma_de_pagamento = st.selectbox("Forma de Pagamento", opcoes_pagamento)
    
    if forma_de_pagamento == 'À Vista':
        parcelas = 0
        valor_entrada = preco
        valor_parcelas = 0
        preco_final = preco + custos_adicionais
    else:
        parcelamento = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        parcelas = st.selectbox("Número de Parcelas", parcelamento)
        valor_entrada = st.number_input('Valor Pago na Entrada', step=0.01, format="%.2f")
        valor_parcelas = st.number_input('Valor das Parcelas', step=0.01, format="%.2f")
        preco_final = parcelas * valor_parcelas + valor_entrada
    preco_unitario = preco_final * quantidade
    registrar = st.button('Registrar Compra')
    if registrar:
        st.session_state.logged_in = True
        st.experimental_rerun()

def criar_dataframe():
    cursor.execute('SELECT * FROM compras')
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df
                                         
def dashboard():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        df_compras = criar_dataframe()
        st.dataframe(df_compras)

registrar_produto()
registrar_compra()
acesso()
gerar_id_unico()
coleta()
inserir_dados()
criar_dataframe()
dashboard()