import streamlit as st

def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        st.success("Login bem-sucedido!")

def cadastrar():
    st.title("Cadastro")
    new_username = st.text_input("Novo Usuário")
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    if new_password != confirm_password:
        st.error("As senhas não coincidem.")
    elif st.button("Cadastrar"):
        st.success("Cadastro realizado com sucesso!")

def main():
    st.set_page_config(page_title='GADM')

    choice = st.sidebar.radio("Escolha uma opção", ["Login", "Cadastro"])

    if choice == "Login":
        login()
    elif choice == "Cadastro":
        cadastrar()

if __name__ == "__main__":
    main()