import streamlit as st
import sqlite3
import random
import string

conn = sqlite3.connect('dados_compras.db')
cursor = conn.cursor()

def registrar_produto():
    cursor.execute('CREATE TABLE IF NOT EXISTS novas_produtos (id_produto TEXT PRIMARY KEY, produto TEXT NOT NULL, modelo TEXT NOT NULL, tamanho TEXT NOT NULL)')
    conn.commit()

def registrar_compra():
        cursor.execute('CREATE TABLE IF NOT EXISTS compras (id_produto TEXT PRIMARY KEY, segmento TEXT NOT NULL, produto TEXT NOT NULL, modelo TEXT NOT NULL, tamanho TEXT NOT NULL, genero TEXT NOT NULL, publico TEXT NOT NULL, quantidade INTEGER NOT NULL, data_compra DATE NOT NULL, preco REAL NOT NULL, custos_adicionais REAL NOT NULL, pagamento TEXT NOT NULL, forma_de_pagamento TEXT NOT NULL, parcelas INTEGER NOT NULL, valor_entrada REAL NOT NULL, valor_parcela REAL NOT NULL, data_pagamento DATE NOT NULL, fornecedor TEXT NOT NULL, data_entrega DATE NOT NULL, preco_unitario REAL NOT NULL, preco_final REAL NOT NULL)')
    conn.commit()

def inserir_dados(id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final):
    if produto == 'Novo Produto':
        cursor.execute('INSERT INTO novas_produtos (id_produto, produto, modelo, tamanho) VALUES (?, ?, ?, ?)', (id_produto, produto, modelo, tamanho))
    cursor.execute('INSERT INTO compras (id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcelas, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id_produto, segmento, produto, modelo, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, preco_unitario, preco_final))

def acesso():
    codigo_de_acesso = st.text_input('Código de Acesso', type='password')
    entrar = st.button('Entrar')
    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
    elif entrar:
        st.warning("O código de acesso inserido não foi aceito, tente novamente.")

def gerar_id_unico():
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=5))
    return letras + numeros

def coleta():
    id_produto = gerar_id_unico()
    
    def carregar_opcao_produtos():
        cursor.execute('SELECT produto FROM novas_produtos')
        produtos = cursor.fetchall()
        opcao_produtos.extend([produto[0] for produto in produtos])
    
    opcao_produtos = ['Novo Produto']
    registrar_produto()
    carregar_opcao_produtos()
    
    def custom_sort_key(item):
        return item if item != 'Novo Produto' else 'zzz'
    produtos_ordenados = sorted(produtos, key=custom_sort_key)
    produto = st.selectbox('Produto Comprado', produtos_ordenados)
        
    if produto == 'Novo Produto':
        produto = st.text_input('Novo Produto')
        
    def carregar_opcao_modelos():
        cursor.execute('SELECT modelo FROM novas_produtos')
        modelos = cursor.fetchall()
        opcao_modelos.extend([modelo[0] for modelo in modelos])
    
    opcao_modelos = ['Novo Modelo']
    registrar_produto()
    carregar_opcao_modelos()
    
    def custom_sort_key(item):
        return item if item != 'Novo Modelo' else 'zzz'
    modelos_ordenados = sorted(modelos, key=custom_sort_key)
    modelos = st.selectbox('Modelo Comprado', modelos_ordenados)
        
    if modelos == 'Novo Modelo':
        produto = st.text_input('Novo Modelo')

     nicho = ['Masculino', 'Feminino', 'Unissex']
     genero = st.selectbox('Gênero', nicho)
     faixa = ['Adulto', 'Infantil']
     publico = st.selectbox('Público', faixa)
     data_compra = st.date_input('Data da Compra')
    preco_da_compra = st.number_input('Preço da Compra em Reais', step=0.01, format="%.2f")
    custos_adicionais = st.number_input('Custos Adicionais', step=0.01, format="%.2f")
    paga = ['À Vista', 'Parcelamento']
    pagamento = st.selectbox("Forma de Pagamento", paga)
    opcoes_pagamento = ["Boleto Bancário", "PIX", "Dinheiro Vivo", "Cartão de Crédito", "Cartão de Débito"]
    forma_de_pagamento = st.selectbox("Forma de Pagamento", opcoes_pagamento)
    
    if forma_de_pagamento == 'À Vista':
        parcelamento = 0
        valor_de_entrada = preco_da_compra
        valor_das_parcelas = 0
    else:
        parcelameto = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        parcelas = st.selectbox("Número de Parcelas", parcelamento)
        valor_de_entrada = st.number_input('Valor Pago na Entrada', step=0.01, format="%.2f")
        valor_parcelas = st.number_input('Valor das Parcelas', step=0.01, format="%.2f")

    data_pagamento = st.date_input('Data de Pagamento (à vista ou última parcela)')

    fornecedor = st.text_input('Fornecedor')
    
    data_entrega = st.date_input('Prazo de Entrega')
    
    if (
        (produto != 'Novo Produto' or not)
        and data_compra 
        and preco 
        and custos_adicionais 
        and forma_de_pagamento 
        and data_pagamento 
        and quantidade
        and fornecedor
        and data_entrega

        if forma_de_pagamento == 'À Vista':
            custo_final = preco + custos_adicionais
        else:
            custo_final = valor_parcelas * parcelas + valor_entrada

        if quantidade!= 0:
            custo_unitario = custo_final / quantidade

        cadastrar_compra = st.button('Cadastrar Compra')
        if cadastrar_compra:
            st.success("Compra cadastrada com sucesso!")
        
        st.warning("Preencha todos os campos em branco antes de cadastrar a compra.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    coleta()

conn.close()