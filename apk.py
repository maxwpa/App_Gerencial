import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sqlite3
import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
            data_compra DATETIME NOT NULL,
            preco REAL NOT NULL,
            custos_adicionais REAL NOT NULL,
            pagamento TEXT NOT NULL,
            forma_de_pagamento TEXT NOT NULL,
            parcelas INTEGER NOT NULL,
            valor_entrada REAL NOT NULL,
            valor_parcela REAL NOT NULL,
            data_pagamento DATETIME NOT NULL,
            parcelas_pagas INTERGER NOT NULL,
            parcelas_restantes INTERGER NOT NULL,
            proxima_parcela DATETIME NOT NULL,
            amortizado REAL BOT NULL,
            divida REAL NOT NULL,
            fornecedor TEXT NOT NULL,
            data_entrega DATETIME NOT NULL,
            custo_unitario REAL NOT NULL,
            custo_final REAL NOT NULL
        )
    ''')
    conn.commit()

registrar_compra()
    
def inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes, proxima_parcela, amortizado, divida, fornecedor, data_entrega, custo_unitario, custo_final):
    cursor.execute('''
        INSERT INTO compras (
            id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento,
            forma_de_pagamento, parcelas, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes, proxima_parcela, amortizado, divida, fornecedor, data_entrega, custo_unitario, custo_final
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes, proxima_parcela, amortizado, divida, fornecedor, data_entrega, custo_unitario, custo_final))
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
        st.sidebar.title('Compras')

        paginas = {
            'Cadastro': coleta,
            'Histórico': tabela,
            'Controle': dashboard
        }

        escolha_pagina = st.sidebar.radio('Selecione a Página', list(paginas.keys()))

        paginas[escolha_pagina]()

def coleta():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        st.title('Cadastrar Compra')
        
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

        data_pagamento = st.date_input('Data do Pagamento À Vista ou Primeira Parcela:')
        
        hoje = datetime.now().date()
        relativa_delta = relativedelta(hoje, data_pagamento)
        parcelas_pagas = relativa_delta.years * 12 + relativa_delta.months
        parcelas_restantes = parcelamento - parcelas_pagas
        
        #proxima_parcela = data_pagamento + relativedelta(months=parcelas_pagas + 1)
        
        amortizado = parcelas_pagas * valor_parcela + valor_entrada
        divida = max(parcelamento - parcelas_pagas, 0) * valor_parcela

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
            parcelas_pagas = 0
            parcelas_restantes = 0
            proxima_parcela = data_pagamento
            amortizado = preco
            divida = 0
        else:
            custo_final = valor_parcela * parcelamento + valor_entrada + custos_adicionais
            proxima_parcela = data_pagamento + relativedelta(months=parcelas_pagas)


        custo_unitario = round(custo_unitario, 2)
        custo_final = round(custo_final, 2)

        campos_preenchidos = produto and data_compra and preco and custos_adicionais and forma_de_pagamento and data_pagamento and quantidade and fornecedor and data_entrega

        registrar_compra = st.button('Registrar Compra', disabled=not campos_preenchidos)

        if registrar_compra:
            if campos_preenchidos:
                inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcelamento, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes, proxima_parcela, amortizado, divida, fornecedor, data_entrega, custo_unitario, custo_final)

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
        
        if filtro_produto or filtro_tamanho or filtro_genero or filtro_publico or filtro_fornecedor:
            df_compras_filtrado = df_compras[
                (df_compras['produto'].isin(filtro_produto) if filtro_produto else True) &
                (df_compras['tamanho'].isin(filtro_tamanho) if filtro_tamanho else True) &
                (df_compras['genero'].isin(filtro_genero) if filtro_genero else True) &
                (df_compras['publico'].isin(filtro_publico) if filtro_publico else True) &
                (df_compras['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)]
            st.dataframe(df_compras_filtrado)
        else:
            st.dataframe(df_compras)
            
def plot_pie_chart(df, image_width=300, image_height=260):
    df_agrupado = df.groupby('produto')['custo_final'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(image_width / 70, image_height / 70))
    
    
    font_size = 7.5
    
    wedges, texts, autotexts = ax.pie(
        df_agrupado['custo_final'],
        labels=df_agrupado['produto'],
        autopct='%1.1f%%',
        startangle=90,
        textprops=dict(color="w", size=font_size, weight='bold'),
        wedgeprops=dict(width=0.4)
    )

    ax.axis('equal')

    
    for text in texts + autotexts:
        text.set_fontsize(font_size)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close(fig)

    return image_stream
            
def dashboard():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        df_compras = criar_dataframe()

        filtro_produto = st.sidebar.multiselect('Filtrar por Produto', df_compras['produto'].unique())
        filtro_tamanho = st.sidebar.multiselect('Filtrar por Tamanho', df_compras['tamanho'].unique())
        filtro_genero = st.sidebar.multiselect('Filtrar por Gênero', df_compras['genero'].unique())
        filtro_publico = st.sidebar.multiselect('Filtrar por Público', df_compras['publico'].unique())
        filtro_fornecedor = st.sidebar.multiselect('Filtrar por Fornecedor', df_compras['fornecedor'].unique())

        if filtro_produto or filtro_tamanho or filtro_genero or filtro_publico or filtro_fornecedor:
            df_compras_filtrado = df_compras[
                (df_compras['produto'].isin(filtro_produto) if filtro_produto else True) &
                (df_compras['tamanho'].isin(filtro_tamanho) if filtro_tamanho else True) &
                (df_compras['genero'].isin(filtro_genero) if filtro_genero else True) &
                (df_compras['publico'].isin(filtro_publico) if filtro_publico else True) &
                (df_compras['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)]
            gasto_total = df_compras_filtrado['custo_final'].sum()
            qtd_comprada = df_compras_filtrado['quantidade'].sum()
            mais_comprado = df_compras_filtrado['produto'].value_counts().idxmax()
            pri_fornecedor = df_compras_filtrado['fornecedor'].value_counts().idxmax()
            contas_pagas = df_compras_filtrado['amortizado'].sum() + df_compras_filtrado['custos_adicionais'].sum()
            dividas = df_compras_filtrado['divida'].sum()
            pagamentos_restantes = df_compras_filtrado['parcelas_restantes'].sum()
            proximo_pagamento = df_compras_filtrado['proxima_parcela'].min()

            pie_chart_stream = plot_pie_chart(df_compras_filtrado)

        else:
            gasto_total = df_compras['custo_final'].sum()
            qtd_comprada = df_compras['quantidade'].sum()
            mais_comprado = df_compras['produto'].value_counts().idxmax()
            pri_fornecedor = df_compras['fornecedor'].value_counts().idxmax()
            contas_pagas = df_compras['amortizado'].sum() + df_compras['custos_adicionais'].sum()
            dividas = df_compras['divida'].sum()
            pagamentos_restantes = df_compras['parcelas_restantes'].sum()
            proximo_pagamento = df_compras['proxima_parcela'].min()
            
            pie_chart_stream = plot_pie_chart(df_compras)
            
        col_a1, col_a2, col_a3, col_a4 = st.columns(4)

        with col_a1:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1);">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Gasto Total</h2>
                        <h1 style="color: #4CAF50; font-size: 25px; font-weight: normal; margin-top: -38px;">R${gasto_total:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a2:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Quantidade Comprada</h2>
                        <h1 style="color: #4CAF50; font-size: 30px; font-weight: normal; margin-top: -40px;">{qtd_comprada}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a3:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Prod. Mais Comprado</h2>
                        <h1 style="color: #4CAF50; font-size: 20px; font-weight: normal; margin-top: -35px;">{mais_comprado}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a4:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Principal Fornecedor</h2>
                        <h1 style="color: #4CAF50; font-size: 20px; font-weight: normal; margin-top: -35px;">{pri_fornecedor}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
            
        st.write("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)

        with col_b1:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Total Pago</h2>
                        <h1 style="color: #4CAF50; font-size: 25px; font-weight: normal; margin-top: -38px;">R${contas_pagas:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_b2:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Dívida</h2>
                        <h1 style="color: #4CAF50; font-size: 25px; font-weight: normal; margin-top: -38px;">R${dividas:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_b3:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Qtd. Contas à Pagar</h2>
                        <h1 style="color: #4CAF50; font-size: 30px; font-weight: normal; margin-top: -40px;">{pagamentos_restantes}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_b4:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 150px; height: 50px; font-family: 'Arial', sans-serif; background-color: #7FFFD4; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #008080; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Próximo Pagamento</h2>
                        <h1 style="color: #4CAF50; font-size: 20px; font-weight: normal; margin-top: -35px;">{proximo_pagamento}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
        
        colu1, colu2 = st.columns(2)
       
        with colu1:
            image_base64 = base64.b64encode(pie_chart_stream.getvalue()).decode()
            html_code = f"""
                <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 250px; height: 195px; font-family: 'Arial', sans-serif; background-color: #008080; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                    <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Gasto Por Produto</h2>
                    <img src="data:image/png;base64, {image_base64}" alt="Gastos Por Produtos" style="width: 220px; height: 190px; border-radius: 10px;">
                </div>
            """
        st.markdown(html_code, unsafe_allow_html=True)

conn.commit()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    indice_paginas()