import streamlit as st
import sqlite3
from datetime import datetime

def criar_tabela():
    conn = sqlite3.connect("dados_compras.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            tipo_produto TEXT,
            tamanho TEXT,
            genero TEXT,
            faixa_etaria TEXT,
            quantidade INTEGER,
            data_compra DATE,
            preco REAL,
            custos_adicionais REAL,
            forma_pagamento TEXT,
            parcelas INTEGER,
            valor_entrada REAL,
            valor_parcelas REAL,
            data_pagamento DATE,
            fornecedor TEXT,
            data_entrega DATE
        )
    ''')
    
    conn.commit()
    conn.close()

def inserir_dados(produto, tipo_produto, tamanho, genero, faixa_etaria, quantidade, data_compra, preco, custos_adicionais,
                  forma_pagamento, parcelas, valor_entrada, valor_parcelas, data_pagamento, fornecedor, data_entrega):
    conn = sqlite3.connect("dados_compras.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO compras (
            produto, tipo_produto, tamanho, genero, faixa_etaria, quantidade, data_compra, preco, custos_adicionais,
            forma_pagamento, parcelas, valor_entrada, valor_parcelas, data_pagamento, fornecedor, data_entrega
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (produto, tipo_produto, tamanho, genero, faixa_etaria, quantidade, data_compra, preco, custos_adicionais,
          forma_pagamento, parcelas, valor_entrada, valor_parcelas, data_pagamento, fornecedor, data_entrega))
    
    conn.commit()
    conn.close()

criar_tabela()

def acesso():
    codigo_de_acesso = st.text_input('Código de Acesso', type='password')
    entrar = st.button('Entrar')
    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
    elif entrar:
        st.warning("O código de acesso inserido não foi aceito, tente novamente.")

def coleta():
    segmentacao = ['Vestuário e Moda']
    segmento = st.selectbox('Segmento', segmentacao)
    
    if segmento == 'Vestuário e Moda':
        produtos = ['Novo Produto']

        def custom_sort_key(a1):
            return a1 if a1 != 'Novo Produto' else 'zzz'
        
        produtos_ordenados = sorted(produtos, key=custom_sort_key)
        produto_comprado = st.selectbox('Produto Comprado', produtos_ordenados)

        if produto_comprado == 'Novo Produto':
            novo_produto = st.text_input('Novo Produto, Ex: camisa, calça, calçado, acessórios, etc...')
            if novo_produto:
                produtos = produtos.append(novo_produto)
        
        tipo_de_produto = ['Novo Tipo']
        
        def custom_sort_key(a2):
            return a2 if a2 != 'Novo Tipo' else 'zzz'
        
        tipo_ordenados = sorted(tipo_de_produto, key=custom_sort_key)
        tipo_comprado = st.selectbox('Tipo de produto', tipo_ordenados)
        
        if tipo_comprado ==  'Novo Tipo':
            novo_tipo = st.text_input('Tipo de Produto, Ex: camisa polo, calça jeans, tênis, boné, etc.')
            if novo_tipo:
                tipo_de_produto = tipo_de_produto.append(novo_tipo)

        tamanho = st.text_input("Tamanho, Ex: P, M, G, GG ou 34, 36, 38, 40; Digite N se o produto não tiver variação de tamanho")
        nicho = ['Masculino', 'Feminino', 'Unissex']
        genero = st.selectbox('Gênero', nicho)
        faixa = ['Adulto', 'Infantil']
        idade = st.selectbox('Público', faixa)

    quantidade_comprada = st.number_input("Quantidade Comprada", step=1, format="%d")
    data_da_compra = st.date_input('Data da Compra')
    preco_da_compra = st.number_input('Preço da Compra em Reais', step=0.01, format="%.2f")
    custos_adicionais = st.number_input('Custos Adicionais', step=0.01, format="%.2f")

    opcoes_pagamento = ["Boleto Bancário", "PIX", "Dinheiro Vivo", "Cartão de Crédito", "Cartão de Débito"]
    forma_de_pagamento = st.selectbox("Forma de Pagamento", opcoes_pagamento)

    pagamento = ['À Vista', 'Parcelamento']
    forma_de_pagamento = st.selectbox("Forma de Pagamento", pagamento)
    
    if forma_de_pagamento == 'À Vista':
        parcelamento = 0
        valor_de_entrada = preco_da_compra
        valor_das_parcelas = 0
    else:
        parcelas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        parcelamento = st.selectbox("Número de Parcelas", parcelas)
        valor_de_entrada = st.number_input('Valor Pago na Entrada', step=0.01, format="%.2f")
        valor_das_parcelas = st.number_input('Valor das Parcelas', step=0.01, format="%.2f")

    data_de_pagamento = st.date_input('Data de Pagamento (à vista ou última parcela)')

    fornecedor = st.text_input('Fornecedor')
    
    data_de_entrega = st.date_input('Prazo de Entrega')

    if (
        (produto_comprado != 'Novo Produto' or novo_produto)
        and data_da_compra 
        and preco_da_compra 
        and custos_adicionais 
        and forma_de_pagamento 
        and data_de_pagamento 
        and quantidade_comprada 
        and fornecedor
        and data_de_entrega
    ):
        if forma_de_pagamento == 'À Vista':
            custo_final = preco_da_compra + custos_adicionais
        else:
            custo_final = valor_das_parcelas * parcelamento + valor_de_entrada

        if quantidade_comprada != 0:
            custo_unitario = custo_final / quantidade_comprada

        cadastrar_compra = st.button('Cadastrar Compra')
        if cadastrar_compra:
            st.success("Compra cadastrada com sucesso!")
        
        inserir_dados(
            produto_comprado if produto_comprado != 'Novo Produto' else novo_produto,
            tipo_comprado if tipo_comprado != 'Novo Tipo' else novo_tipo,
            tamanho, genero, idade, quantidade_comprada,
            data_da_compra, preco_da_compra, custos_adicionais,
            forma_de_pagamento, parcelamento, valor_de_entrada, valor_das_parcelas, data_de_pagamento,
            fornecedor, data_de_entrega
        )
        
    else:
        st.warning("Preencha todos os campos em branco antes de cadastrar a compra.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    coleta()