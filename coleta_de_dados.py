import streamlit as st

def acesso():
    codigo_de_acesso = st.text_input('Código de Acesso', type='password')
    entrar = st.button('Entrar')
    if entrar and codigo_de_acesso == "20210088628":
        st.session_state.logged_in = True
        st.success("Login bem-sucedido!")
    elif entrar:
        st.warning("O código de acesso inserido não foi aceito, tente outro.")

def coleta():
    produto_comprado = st.text_input('Produto Comprado')
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

    data_de_pagamento = st.date_input('Data de Pagamento')
    quantidade_comprada = st.number_input("Quantidade Comprada", step=1, format="%d")
    fornecedor = st.text_input('Fornecedor')

    if (
        produto_comprado 
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
