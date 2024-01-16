import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sqlite3
import random
import string
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import FuncFormatter
from streamlit import components
import numpy as np

import altair as alt













st.set_page_config(page_title='SGN')

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
            parcelas_pagas INTEGER NOT NULL,
            parcelas_restantes INTEGER NOT NULL,
            proxima_data DATETIME NOT NULL,
            proxima_parcela INTEGER NOT NULL,
            amortizado REAL BOT NULL,
            divida REAL NOT NULL,
            fornecedor TEXT NOT NULL,
            data_entrega DATETIME NOT NULL,
            juros INTEGER NOT NULL,
            custo_unitario REAL NOT NULL,
            custo_final REAL NOT NULL
        )
    ''')
    conn.commit()

registrar_compra()
    
def inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes,  proxima_data, proxima_parcela, amortizado, divida, fornecedor, data_entrega, juros, custo_unitario, custo_final):
    cursor.execute('''
        INSERT INTO compras (
            id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento,
            forma_de_pagamento, parcelas, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes,  proxima_data, proxima_parcela, amortizado, divida, fornecedor, data_entrega, juros, custo_unitario, custo_final
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcela, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes,  proxima_data, proxima_parcela, amortizado, divida, fornecedor, data_entrega, juros, custo_unitario, custo_final))
    conn.commit()
    
def registrar_datas():
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datas (
            data DATETIME NOT NULL,
            custo REAL NOT NULL,
            produto TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            genero TEXT NOT NULL,
            publico TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            meses DATETIME NOT NULL,
            anos DATETIME NOT NULL,
            FOREIGN KEY (produto) REFERENCES compras(produto),
            FOREIGN KEY (tamanho) REFERENCES compras(tamanho),
            FOREIGN KEY (genero) REFERENCES compras(genero),
            FOREIGN KEY (publico) REFERENCES compras(publico),
            FOREIGN KEY (fornecedor) REFERENCES compras(fornecedor)
        )
    ''')
    conn.commit()
    
registrar_datas()

def inserir_datas(data_compra, data_pagamento, preco, custos_adicionais, pagamento, parcelamento, valor_parcela, parcelas_pagas, valor_entrada, produto, tamanho, genero, publico, fornecedor):
    
    nome_mes_compra = datetime.strftime(data_compra, "%B")
    
    if pagamento == 'À Vista':
        cursor.execute('''
            INSERT INTO datas (data, custo, produto, tamanho, genero, publico, fornecedor, meses, anos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data_compra, preco + custos_adicionais, produto, tamanho, genero, publico, fornecedor, nome_mes_compra, data_compra.year))
    else:
        cursor.execute('''
            INSERT INTO datas (data, custo, produto, tamanho, genero, publico, fornecedor, meses, anos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data_compra, valor_entrada + custos_adicionais, produto, tamanho, genero, publico, fornecedor, nome_mes_compra, data_compra.year))

    if pagamento != 'À Vista':
        for i in range(parcelamento):
            data_parcela = data_pagamento + relativedelta(months=i)
            nome_mes_parcela = datetime.strftime(data_parcela, "%B")
            
            cursor.execute('''
                INSERT INTO datas (data, custo, produto, tamanho, genero, publico, fornecedor, meses, anos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data_parcela, valor_parcela, produto, tamanho, genero, publico, fornecedor, nome_mes_parcela, data_parcela.year))

    conn.commit()


def acesso():
    
    st.title('Bem-vindo ao SGN')
    st.text('Sistema de Gerenciamento de Negócios')
    
    #st.write("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text('')
    
    with col2:
        codigo_de_acesso = st.text_input('Código de Acesso', type='password')
        entrar = st.button('Entrar')
    
    with col3:
        st.text('')

    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
    elif entrar:
        st.warning("Código de acesso incorreto. Tente novamente.")

        
    back_image = "https://www.10wallpaper.com/wallpaper/1680x1050/1411/Cool_Black_3D-Abstract_widescreen_wallpaper_1680x1050.jpg" 
    
    page_bg_img = '''
    <style>
        .stApp {
            background-image: url("%s");
            background-size: cover;
        }
    </style>
''' % back_image

    st.markdown(page_bg_img, unsafe_allow_html=True)
        

def indice_paginas():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:    
        st.sidebar.title('Compras')

        paginas = {
            'Cadastro': coleta,
            'Registros': tabela,
            'Gerenciamento': dashboard
        }

        escolha_pagina = st.sidebar.radio('Selecione a Página', list(paginas.keys()))

        paginas[escolha_pagina]()
        
        back_image = "https://cutewallpaper.org/21/good-wallpaper-for-iphone-6/30-Best-Cool-Retina-iPhone-6-Wallpapers-Backgrounds-in-HD-.jpg" 
    
        page_bg_img = '''
        <style>
            .stApp {
                background-image: url("%s");
                background-size: cover;
            }
        </style>
    ''' % back_image

        st.markdown(page_bg_img, unsafe_allow_html=True)

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

        data_pagamento = st.date_input('Data do Pagamento À Vista ou Primeira Parcela:', datetime.now().date())
        
        hoje = datetime.now().date()

        par_pagas = relativedelta(hoje, data_pagamento)

        if hoje <= data_pagamento:
            parcelas_pagas = 0
        else:
            parcelas_pagas = par_pagas.years * 12 + par_pagas.months + 1

        parcelas_restantes = parcelamento - parcelas_pagas
        
        amortizado = parcelas_pagas * valor_parcela + valor_entrada
        divida = parcelas_restantes * valor_parcela

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
            proxima_data = 'VENCEU'
            proxima_parcela = 'VENCEU'
            amortizado = preco
            divida = 0
        else:
            custo_final = valor_parcela * parcelamento + valor_entrada + custos_adicionais
            if parcelas_restantes > 0:
                proxima_data = data_pagamento + relativedelta(months=parcelas_pagas)
                diferenca = proxima_data - hoje
                proxima_parcela = diferenca.days
            else:
                proxima_data = 'VENCEU'
                proxima_parcela = 'VENCEU'
        if amortizado + divida - preco == 0:
            juros = 0
        else:
            juros = (amortizado + divida - preco) / preco
        custo_unitario = round(custo_unitario, 2)
        custo_final = round(custo_final, 2)

        campos_preenchidos = produto and data_compra and preco and custos_adicionais and forma_de_pagamento and data_pagamento and quantidade and fornecedor and data_entrega

        registrar_compra = st.button('Registrar Compra', disabled=not campos_preenchidos)

        if registrar_compra:
            if campos_preenchidos:
                inserir_dados(id_produto, produto, tamanho, genero, publico, quantidade, data_compra, preco, custos_adicionais, pagamento, forma_de_pagamento, parcelamento, valor_entrada, valor_parcela, data_pagamento, parcelas_pagas, parcelas_restantes, proxima_data, proxima_parcela, amortizado, divida, fornecedor, data_entrega, juros, custo_unitario, custo_final)
                
                inserir_datas(data_compra, data_pagamento, preco, custos_adicionais, pagamento, parcelamento, valor_parcela, parcelas_pagas, valor_entrada, produto, tamanho, genero, publico, fornecedor)
                
                st.success("Compra cadastrada com sucesso!") 
            else:
                st.warning("Preencha todos os campos em branco antes de cadastrar a compra.")     

                
def carregar_dados():
    
    df_compras = pd.read_sql_query('SELECT * FROM compras', conn)
    df_datas = pd.read_sql_query('SELECT * FROM datas', conn)
    return df_compras, df_datas          
                
def tabela():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        st.title('Histórico de Compras')
        
        df_compras, df_datas = carregar_dados()

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
                (df_compras['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)].copy()

            df_datas_filtrado = df_datas[
                (df_datas['produto'].isin(filtro_produto) if filtro_produto else True) &
                (df_datas['tamanho'].isin(filtro_tamanho) if filtro_tamanho else True) &
                (df_datas['genero'].isin(filtro_genero) if filtro_genero else True) &
                (df_datas['publico'].isin(filtro_publico) if filtro_publico else True) &
                (df_datas['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)].copy()
    
            st.subheader('Compras Filtradas')
            st.dataframe(df_compras_filtrado)

            st.subheader('Datas Filtradas')
            st.dataframe(df_datas_filtrado)
            
        else:
            
            st.subheader('Compras')
            st.dataframe(df_compras)

            st.subheader('Datas')
            st.dataframe(df_datas)
            
            
            
def plot_pie_chart(df, image_width=1000, image_height=860):
    df_agrupado = df.groupby('produto')['custo_final'].sum().reset_index()
    
    colors = plt.cm.Set1.colors

    fig, ax = plt.subplots(figsize=(image_width / 100, image_height / 140))

    font_size = 20
    
    total_custo = df_agrupado['custo_final'].sum()
    
    df_agrupado_top5 = df_agrupado.nlargest(4, 'custo_final')

    
    produtos_dict = {produto: produto if produto in df_agrupado_top5['produto'].values else 'OUTROS' for produto in df_agrupado['produto']}
    
  
    df['produto_agrupado'] = df['produto'].map(produtos_dict)

    df_agrupado = df.groupby('produto_agrupado')['custo_final'].sum().reset_index()

    wedges, texts, autotexts = ax.pie(
        df_agrupado['custo_final'],
        labels=[f"{produto}\n(R${valor:.2f})" for produto, valor in zip(df_agrupado['produto_agrupado'], df_agrupado['custo_final'])],
        autopct=lambda p: '{:.1f}%'.format(p) if p > 5 else '',
        startangle=90,
        textprops=dict(color="w", size=font_size, weight='bold'),
        wedgeprops=dict(width=0.4),
        radius=0.9,
        colors=colors
    )

    ax.axis('equal')

    for text, autotext in zip(texts, autotexts):
        text.set_fontsize(font_size)
        autotext.set_fontsize(font_size)
        autotext.set_bbox(dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='black', lw=2))

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close(fig)

    return image_stream


#def plot_pie_chart_altair(df, image_width=400, image_height=400):
#    df_agrupado = df.groupby('produto')['custo_final'].sum().reset_index()
    
#    colors = alt.Color('produto:N', scale=alt.Scale(scheme='category20b'))
    
#    total_custo = df_agrupado['custo_final'].sum()
    
#    df_agrupado_top5 = df_agrupado.nlargest(4, 'custo_final')
    
#    produtos_dict = {produto: produto if produto in df_agrupado_top5['produto'].values else 'OUTROS' for produto in df_agrupado['produto']}
    
##    df['produto_agrupado'] = df['produto'].map(produtos_dict)
    
##    df_agrupado = df.groupby('produto_agrupado')['custo_final'].sum().reset_index()

##    chart = alt.Chart(df_agrupado).mark_arc().encode(
##        theta='custo_final:Q',
##        color=colors,
##        tooltip=['produto_agrupado:N', 'custo_final:Q']
##    ).transform_calculate(
##        Porcentagem='datum.custo_final / ' + str(total_custo)
##    )

##    labels = alt.Chart(df_agrupado).mark_text(align='center', baseline='middle').encode(
##        text='produto_agrupado:N',
##        detail='produto_agrupado:N',
##        color=alt.value('white'),
##        tooltip=['produto_agrupado:N', 'Porcentagem:Q'],
##        angle=alt.value(0),
##        radius=alt.value(100),
##    ).transform_calculate(
##        Porcentagem='datum.custo_final / ' + str(total_custo)
##    ).properties(width=image_width, height=image_height)

##    chart_final = (chart + labels).configure_view(stroke=None)

##    image_stream = BytesIO()
##    chart_final.save(image_stream, format='png', scale_factor=2.0, method='selenium', webdriver='chrome', webdriver_options=['--headless', '--disable-gpu', '--no-sandbox'])
##    image_stream.seek(0)

##    return image_stream




#def quantidade_por_fornecedor_setores(df, image_width=1000, image_height=860):
#    df_agrupado = df.groupby('fornecedor')['quantidade'].sum().reset_index()

#    colors = plt.cm.Set2.colors

#    fig, ax = plt.subplots(figsize=(image_width / 100, image_height / 140))

#    font_size = 20

#    total_quantidade = df_agrupado['quantidade'].sum()

#    df_agrupado_top5 = df_agrupado.nlargest(4, 'quantidade')

#    fornecedores_dict = {fornecedor: fornecedor if fornecedor in df_agrupado_top5['fornecedor'].values else 'OUTROS' for fornecedor in df_agrupado['fornecedor']}
    
#    df['fornecedor_agrupado'] = df['fornecedor'].map(fornecedores_dict)

#    df_agrupado = df.groupby('fornecedor_agrupado')['quantidade'].sum().reset_index()

#    wedges, texts, autotexts = ax.pie(
#        df_agrupado['quantidade'],
#        labels=[f"{fornecedor} ({quantidade:.0f})" for fornecedor, quantidade in zip(df_agrupado['fornecedor_agrupado'], df_agrupado['quantidade'])],
#        autopct=lambda p: '{:.1f}%'.format(p),
#        startangle=90,
#        textprops=dict(color="w", size=font_size, weight='bold'),
##        wedgeprops=dict(width=0.4),
##        radius=0.9,
##        colors=colors
#    )

#    ax.axis('equal')

#    for text, autotext in zip(texts, autotexts):
#        text.set_fontsize(font_size)
#        autotext.set_fontsize(font_size)
#        autotext.set_bbox(dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='black', lw=2))

#    image_stream = BytesIO()
#    plt.savefig(image_stream, format='png', transparent=True)
#    plt.close(fig)

#    return image_stream

def quantidade_por_fornecedor(df, image_width=1000, image_height=860):
    df_agrupado = df.groupby('fornecedor')['quantidade'].sum().reset_index()

    colors = plt.cm.Set2.colors

    fig, ax = plt.subplots(figsize=(image_width / 100, image_height / 140))

    font_size = 20

    total_quantidade = df_agrupado['quantidade'].sum()

    df_agrupado_top5 = df_agrupado.nlargest(4, 'quantidade')

    fornecedores_dict = {fornecedor: fornecedor if fornecedor in df_agrupado_top5['fornecedor'].values else 'OUTROS' for fornecedor in df_agrupado['fornecedor']}
    
    df['fornecedor_agrupado'] = df['fornecedor'].map(fornecedores_dict)

    df_agrupado = df.groupby('fornecedor_agrupado')['quantidade'].sum().reset_index()

    bars = ax.barh(df_agrupado['fornecedor_agrupado'], df_agrupado['quantidade'], color=colors)

    ax.tick_params(axis='y', labelrotation=0, labelsize=font_size)
    ax.tick_params(axis='x', labelsize=font_size)

    for i, (fornecedor, quantidade) in enumerate(zip(df_agrupado['fornecedor_agrupado'], df_agrupado['quantidade'])):
        ax.text(0, i, f"{fornecedor} ({quantidade})", ha='left', va='center', color='black', fontweight='bold', fontsize=font_size)

    for bar in bars:
        percentage = (bar.get_width() / total_quantidade) * 100
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{percentage:.1f}%", ha='left', va='center', color='white', fontweight='bold', bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'), fontsize=font_size)

    ax.grid(False)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close(fig)

    return image_stream


#    monthly_means = df.groupby(df['data'].dt.to_period("M")).agg({'custo': 'mean'}).reset_index()
#    for i, row in monthly_means.iterrows():      
#        bbox_props = dict(boxstyle="round,pad=0.3", fc="black", ec="black", lw=2)
#        ax.text(row['data'].to_timestamp(), row['custo'], f'{row["custo"]:.2f}', ha="center", va="center", bbox=bbox_props, color='white', fontsize=10, fontweight='bold')

#    count_custo = df.groupby(df['data'].dt.to_period("M")).agg({'custo': 'count'}).reset_index()

#    for i, row in count_custo.iterrows():
#        bbox_props = dict(boxstyle="round,pad=0.3", fc="black", ec="black", lw=2)
#        ax.text(row['data'].to_timestamp(), row['custo'], f'{row["custo"]:.0f}', ha="center", va="center", bbox=bbox_props, color='white', fontsize=10, fontweight='bold')



def grafico_barras(df, image_width=2000, image_height=886, indice_fontsize=18):
    df['data'] = pd.to_datetime(df['data'])
    df['custo'] = pd.to_numeric(df['custo'], errors='coerce')
    df = df.sort_values(by='data')

    fig, ax = plt.subplots(figsize=(image_width/100, image_height/175))

    total_custo = df.groupby(df['data'].dt.to_period("M")).agg({'custo': 'sum'}).reset_index()
    total_custo['data'] = total_custo['data'].dt.to_timestamp() 

    ax.bar(total_custo['data'], total_custo['custo'], color='lightgray', label='Total')

    ax.plot(df['data'], df['custo'], color='red', marker='o')
    ax.fill_between(df['data'], df['custo'], color='blue', alpha=0.4)

    mean_custo = df['custo'].mean()
    ax.axhline(y=mean_custo, color='orange', linestyle='--', label=f'Média: R${mean_custo:.2f}')

    for i, row in total_custo.iterrows():
        bbox_props = dict(boxstyle="round,pad=0.3", fc="black", ec="black", lw=2)
        ax.text(row['data'], row['custo'], f'{row["custo"]:.2f}', ha="center", va="center", bbox=bbox_props, color='white', fontsize=16, fontweight='bold')

    count_custo = df.groupby(df['data'].dt.to_period("M")).agg({'custo': 'count'}).reset_index()

    for i, row in count_custo.iterrows():
        bbox_props = dict(boxstyle="round,pad=0.3", fc="black", ec="black", lw=2)
        ax.text(row['data'].to_timestamp(), row['custo'], f'{row["custo"]:.0f}', ha="center", va="center", bbox=bbox_props, color='white', fontsize=16, fontweight='bold')

    plt.xticks(fontweight='bold', color='white', fontsize=18)
    #ax.legend()
    ax.tick_params(axis='y', labelcolor='white', labelsize=18)
    ax.tick_params(axis='y', labelsize=indice_fontsize)
    ax.set_yticklabels([f'R${val:.0f}' for val in ax.get_yticks()])
    ax.grid(False)

    for spine in ax.spines.values():
        spine.set_visible(False)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    image_stream.seek(0)

    plt.clf()
    plt.close()

    return image_stream


            
def dashboard():
    if hasattr(st.session_state, 'logged_in') and st.session_state.logged_in:
        st.title('Gerenciamento')
        
        df_compras = pd.read_sql_query('SELECT * FROM compras', conn)
        df_datas = pd.read_sql_query('SELECT * FROM datas', conn)

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
                (df_compras['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)].copy()

            df_datas_filtrado = df_datas[
                (df_datas['produto'].isin(filtro_produto) if filtro_produto else True) &
                (df_datas['tamanho'].isin(filtro_tamanho) if filtro_tamanho else True) &
                (df_datas['genero'].isin(filtro_genero) if filtro_genero else True) &
                (df_datas['publico'].isin(filtro_publico) if filtro_publico else True) &
                (df_datas['fornecedor'].isin(filtro_fornecedor) if filtro_fornecedor else True)].copy()
            
            
            gasto_total = df_compras_filtrado['custo_final'].sum()
            qtd_comprada = df_compras_filtrado['quantidade'].sum()
            mais_comprado = df_compras_filtrado['produto'].value_counts().idxmax()
            pri_fornecedor = df_compras_filtrado['fornecedor'].value_counts().idxmax()
            contas_pagas = df_compras_filtrado['amortizado'].sum() + df_compras_filtrado['custos_adicionais'].sum()
            dividas = df_compras_filtrado['divida'].sum()
            pagamentos_restantes = df_compras_filtrado['parcelas_restantes'].sum()
            dias_falta = df_compras_filtrado['proxima_parcela'].min()
            custo_peca = df_compras_filtrado['custo_unitario'].mean()
            
            pie_chart_stream = plot_pie_chart(df_compras_filtrado)
            qtd_fornecedor = quantidade_por_fornecedor(df_compras_filtrado)
            custo_meses = grafico_barras(df_datas_filtrado)

        else:
            gasto_total = df_compras['custo_final'].sum()
            qtd_comprada = df_compras['quantidade'].sum()
            mais_comprado = df_compras['produto'].value_counts().idxmax()
            pri_fornecedor = df_compras['fornecedor'].value_counts().idxmax()
            contas_pagas = df_compras['amortizado'].sum() + df_compras['custos_adicionais'].sum()
            dividas = df_compras['divida'].sum()
            pagamentos_restantes = df_compras['parcelas_restantes'].sum()
            dias_falta = df_compras['proxima_parcela'].min()
            custo_peca = df_compras['custo_unitario'].mean()
            
            pie_chart_stream = plot_pie_chart(df_compras)
            qtd_fornecedor = quantidade_por_fornecedor(df_compras)
            custo_meses = grafico_barras(df_datas)
            
        if dias_falta != 'VENCEU':
            if dias_falta == 1:
                vencimento = 'AMANHÃ'
            elif dias_falta == 0:
                vencimento = 'HOJE'
            else:
                vencimento = f'EM {dias_falta} DIAS'
        else:
                vencimento = 'VENCEU'
        
        preco_recomendado = custo_peca * 0.3 + custo_peca
            
        col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)

        with col_a1:
            st.markdown(
                f"""
                    <div style="border: 3px dashed #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #A52A2A; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1);">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Gasto Total</h2>
                        <h1 style="color: #F5F5DC; font-size: 25px; font-weight: normal; margin-top: -38px;">R${gasto_total:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a2:
            st.markdown(
                f"""
                    <div style="border: 3px dotted #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #556B2F; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Total Pago</h2>
                        <h1 style="color: #F5F5DC; font-size: 25px; font-weight: normal; margin-top: -38px;">R${contas_pagas:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a3:
            st.markdown(
                f"""
                    <div style="border: 3px double #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #2F4F4F; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Contas à Pagar</h2>
                        <h1 style="color: #F5F5DC; font-size: 25px; font-weight: normal; margin-top: -38px;">R${dividas:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_a4:
            st.markdown(
                f"""
                    <div style="border: 3px ridge #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #8B4513; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Qtd. Contas à Pagar</h2>
                        <h1 style="color: #F5F5DC; font-size: 30px; font-weight: normal; margin-top: -40px;">{pagamentos_restantes}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
         
        with col_a5:
            st.markdown(
                f"""
                    <div style="border: 3px groove #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #191970; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Próximo Vencimento</h2>
                        <h1 style="color: #F5F5DC; font-size: 20px; font-weight: normal; margin-top: -35px;">{vencimento}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
            
        st.write("<div style='height: 0px;'></div>", unsafe_allow_html=True)
            
        col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)

        with col_b1:
            st.markdown(
                f"""
                    <div style="border: 3px inset #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #2F4F4F; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Qtd. Comprada</h2>
                        <h1 style="color: #F5F5DC; font-size: 30px; font-weight: normal; margin-top: -40px;">{qtd_comprada}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_b2:
            if len(mais_comprado) <= 12:
                fonte = 20
            else:
                fonte = 19
            st.markdown(
                f"""
                    <div style="border: 3px outset #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #8B4513; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Prod. Mais Comprado</h2>
                        <h1 style="color: #F5F5DC; font-size: {fonte}px; font-weight: normal; margin-top: -35px;">{mais_comprado}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

        with col_b3:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #191970; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Principal Fornecedor</h2>
                        <h1 style="color: #F5F5DC; font-size: 20px; font-weight: normal; margin-top: -35px;">{pri_fornecedor}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
        
        with col_b4:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #800000; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Custo Unitário</h2>
                        <h1 style="color: #F5F5DC; font-size: 25px; font-weight: normal; margin-top: -38px;">R${custo_peca:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)
            
        with col_b5:
            st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 140px; height: 50px; font-family: 'Arial', sans-serif; background-color: #556B2F; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Preço Recomendado</h2>
                        <h1 style="color: #F5F5DC; font-size: 25px; font-weight: normal; margin-top: -38px;">R${preco_recomendado:.2f}</h1>
                    </div>
                """,
                unsafe_allow_html=True)

            
#        plot_pie_chart_altair(df_compras)
            
        st.write("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
       
        with col_c1:
            image_base64 = base64.b64encode(pie_chart_stream.getvalue()).decode()
            st.markdown(
                f"""
                <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 355px; height: 218px; font-family: 'Arial', sans-serif; background-color: #1C1C1C; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                    <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Gasto Por Produto</h2>
                    <img src="data:image/png;base64, {image_base64}" alt="Gastos Por Produtos" style="width: 340px; height: 205px; border-radius: 10px;">
                </div>
            """,
                unsafe_allow_html=True)
        
        with col_c2:
            image_base64 = base64.b64encode(qtd_fornecedor.getvalue()).decode()
            st.markdown(
                f"""
                <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 355px; height: 218px; font-family: 'Arial', sans-serif; background-color: #333333; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                    <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Compras por Fornecedor</h2>
                    <img src="data:image/png;base64, {image_base64}" alt="Qtd. Comprada por Fornecedor" style="width: 340px; height: 205px; border-radius: 10px;">
                </div>
            """,
                unsafe_allow_html=True)
        
        st.write("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        
        image_base64 = base64.b64encode(custo_meses.getvalue()).decode()
        st.markdown(
                f"""
                    <div style="border: 3px solid #e2e2e2; border-radius: 5px; padding: 1px; text-align: center; width: 715px; height: 218px; font-family: 'Arial', sans-serif; background-color: #2F4F4F; box-shadow: inset 0 0 40px rgba(0, 0, 0, 1)">
                        <h2 style="color: #7FFFD4; font-size: 12px; font-weight: bold; margin-bottom: -25px; margin-top: -18px;">Gastos por Mês</h2>
                        <img src="data:image/png;base64, {image_base64}" alt="Gasto Total & Quantidade de Contas por Mês" style="width: 780px; height: 205px; border-radius: 10px; margin-left: -30px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        

conn.commit()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    indice_paginas()