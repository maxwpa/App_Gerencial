import streamlit as st

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
        produtos = [
        "Camiseta",
        'Calça',
            'Jaqueta',
            'Bermuda',
        "Camisas",
        "Vestidos",
        "Blazers",
        "Saia",
        "Casaco",
        "Short",
        "Suéter",
            'Camisa de Bandas',
        "Macacões",
        "Calçados",
        "Acessórios",
            'Produtos de Beleza',
            'Eletrónicos',
        'Novo Produto']
    
        def custom_sort_key(item):
            return item if item != 'Novo Produto' else 'zzz'
        produtos_ordenados = sorted(produtos, key=custom_sort_key)
        produto_comprado = st.selectbox('Produto Comprado', produtos_ordenados)
        if produto_comprado == 'Novo Produto':
            novo_produto = st.text_input('Novo Produto')
        elif: produto_comprado == 'Calçados':
            calcados = [
                    "Tênis esportivo",
                    "Sapatênis",
                    "Sapato social",
                    "Chinelo",
                    "Sandália rasteira",
                    "Sapato de salto alto",
                    "Chuteira",
                    "Alpargata",
                    "Mocassim",
                    "Sapatilha",
                    "Bota de cano alto",
                    "Tênis casual",
                    "Chinelo slide",
                    "Tênis de corrida",
                    "Bota chelsea",
                    'Novo Calçado'
                ]
            def custom_sort_key(item1):
                return item1 if item1 != 'Novo Calçado' else 'zzz'
            calcados_ordenados = sorted(calcados, key=custom_sort_key)
            calcado_comprado = st.selectbox('Calçado Comprado', calcados_ordenados)
            if calcado_comprado == 'Novo Calçado':
                novo_calcado = st.text_input('Novo Calçado')

            tamanho = st.number_imput('Tamanho do Calçado')
            nicho = ['Masculino', 'Feminino', 'Unissex']
            genero = st.selectbox('Gênero', nicho)

        
    data_da_compra = st.date_input('Data da Compra')
    preco_da_compra = st.number_input('Preço da Compra em Reais', step=0.01, format="%.2f")
    custos_adicionais = st.number_input('Custos Adicionais', step=0.01, format="%.2f")

    opcoes_pagamento = ["Boleto Bancário", "PIX", "Dinheiro Vivo", "Cartão de Crédito", "Cartão de Débito"]
    forma_de_pagamento = st.selectbox("Forma de Pagamento", opcoes_pagamento)

    pagamento = ['À Vista', 'Parcelamento']
    forma_de_pagamento = st.selectbox("Forma de Pagamento", pagamento)

    if (
        (produto_comprado != 'Novo Produto' or novo_produto)
        and data_da_compra 
        and preco_da_compra 
        and custos_adicionais 
        and forma_de_pagamento 
        and data_de_pagamento 
        and quantidade_comprada 
        and fornecedor
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
    else:
        st.warning("Preencha todos os campos em branco antes de cadastrar a compra.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    acesso()
else:
    coleta()

