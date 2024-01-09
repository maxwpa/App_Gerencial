import streamlit as st
import pandas as pd
import sqlite3
import random
import string

conn = sqlite3.connect('dados_compras.db')
cursor = conn.cursor()
    
def registrar_compra():
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id_produto TEXT PRIMARY KEY,
            produto TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            genero TEXT NOT NULL,
            publico TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_compra DATE NOT NULL,
            preco REAL NOT NULL,
            custos_adicionais REAL NOT NULL,
            pagamento TEXT NOT NULL,
            forma_de_pagamento TEXT NOT NULL,
            parcelas INTEGER NOT NULL,
            valor_entrada REAL NOT NULL,
            valor_parcela REAL NOT NULL,
            data_pagamento DATE NOT NULL,
            fornecedor TEXT NOT NULL,
            data_entrega DATE NOT NULL,
            custo_unitario REAL NOT NULL,
            custo_final REAL NOT NULL
        )
    ''')
    conn.commit()

registrar_compra()
    
def inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, custo_unitario, custo_final):
    cursor.execute('''
        INSERT INTO compras (
            id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento,
            forma_de_pagamento, parcelas, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, custo_unitario, custo_final
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, custo_unitario, custo_final))
    conn.commit()
    
def acesso():
    codigo_de_acesso = st.text_input('Código de Acesso', type='password')
    entrar = st.button('Entrar')
    
    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
    elif entrar:
        st.warning("Código de acesso incorreto. Tente novamente.")

def indice_paginas():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:    
        st.sidebar.title('Índice de Páginas')

        paginas = {
            'Tabela de Compras': tabela,
            'Registrar Compra': coleta,
            'DashBoard Compras': dashboard
        }

        escolha_pagina = st.sidebar.radio('Selecione a Página', list(paginas.keys()))

        paginas[escolha_pagina]()

def coleta():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        produto = st.text_input('Produto Comprado').upper()

        letras = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join(random.choices(string.digits, k=5))
        id_produto = letras + numeros

        tamanho = st.text_input('Tamanho, ex: G, GG ou 36, 38').upper()
        grupo = ['Masculino', 'Feminino', 'Unissex']
        genero = st.selectbox('Gênero', grupo)
        nicho = ['Adulto', 'Infantil']
        publico = st.selectbox('Público', nicho)
        quantidade = st.number_input("Quantidade Comprada", step=1, format="%d")
        data_compra = st.date_input('Data da Compra')
        preco = st.number_input('Preço da Compra em Reais', step=0.01, format="%.2f")
        custos_adicionais = st.number_input('Custos Adicionais', step=0.01, format="%.2f")

        opcoes_pagamento = ["Boleto Bancário", "PIX", "Dinheiro Vivo", "Cartão de Crédito", "Cartão de Débito"]
        forma_de_pagamento = st.selectbox("Forma de Pagamento", opcoes_pagamento)

        paga = ['À Vista', 'Parcelado']
        pagamento = st.selectbox("Opções de Pagamento", paga)

        if pagamento == 'À Vista':
            parcelamento = 0
            valor_entrada = preco
            valor_parcela = 0
        else:
            parcelas = list(range(1, 13))
            parcelamento = st.selectbox("Número de Parcelas", parcelas)
            valor_entrada = st.number_input('Valor Pago na Entrada', step=0.01, format="%.2f")
            valor_parcela = st.number_input('Valor das Parcelas', step=0.01, format="%.2f")

        data_pagamento = st.date_input('Data de Pagamento (à vista ou última parcela)')

        fornecedor = st.text_input('Fornecedor').upper()

        data_entrega = st.date_input('Prazo de Entrega')

        preco = round(preco, 2)
        custos_adicionais = round(custos_adicionais, 2)

        if quantidade > 0:
            custo_unitario = (preco + custos_adicionais) / quantidade
        else:
            custo_unitario = 0


        if pagamento == 'À Vista':
            custo_final = preco + custos_adicionais
        else:
            custo_final = valor_parcela * parcelamento + valor_entrada + custos_adicionais


        custo_unitario = round(custo_unitario, 2)
        custo_final = round(custo_final, 2)

        campos_preenchidos = produto and data_compra and preco and custos_adicionais and forma_de_pagamento and data_pagamento and quantidade and fornecedor and data_entrega

        registrar_compra = st.button('Registrar Compra', disabled=not campos_preenchidos)

        if registrar_compra:
            if campos_preenchidos:
                inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcelamento, valor_entrada, valor_parcela, data_pagamento, fornecedor, data_entrega, custo_unitario, custo_final)

                st.success("Compra cadastrada com sucesso!")
            else:
                st.warning("Preencha todos os campos em branco antes de cadastrar a compra.")
            
def criar_dataframe():
    cursor.execute('SELECT * FROM compras')
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df

def tabela():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        df_compras = criar_dataframe()
        filtro_produto = st.sidebar.multiselect('Filtrar por Produto', df_compras['produto'].unique())
        filtro_tamanho = st.sidebar.multiselect('Filtrar por Tamanho', df_compras['tamanho'].unique())
        filtro_genero = st.sidebar.multiselect('Filtrar por Gênero', df_compras['genero'].unique())
        filtro_publico = st.sidebar.multiselect('Filtrar por Público', df_compras['publico'].unique())
        filtro_fornecedor = st.sidebar.multiselect('Filtrar por Fornecedor', df_compras['fornecedor'].unique())
        
        if filtro_produto or filtro_tamanho:
            df_compras_filtrado = df_compras[df_compras['produto'].isin(filtro_produto)]
            st.dataframe(df_compras_filtrado)
        else:
            st.dataframe(df_compras)
        
def dashboard():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        df_compras = criar_dataframe()
        st.sidebar.title("Filtros")
        filtro_genero = st.sidebar.multiselect("Filtrar por Gênero",
                                               df_compras["genero"].unique())
        filtro_pagamento = st.sidebar.multiselect("Filtrar por Forma de Pagamento",
                                                  df_compras["forma_de_pagamento"].unique())
        df_filtrado = df_compras[
        (df_compras["genero"].isin(filtro_genero)) &
        (df_compras["forma_de_pagamento"].isin(filtro_pagamento))
    ]
        
        st.subheader("Gráficos Interativos")
        st.line_chart(df_filtrado.groupby("data_compra")["quantidade"].sum(),
                      use_container_width=True)
        st.subheader("Estatísticas")
        st.write("Total de Compras:", df_filtrado.shape[0])
        st.write("Quantidade Total Comprada:", df_filtrado["quantidade"].sum())
        st.write("Custo Total:", df_filtrado["custo_final"].sum())
        
        st.dataframe(df_filtrado)

conn.commit()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    indice_paginas()