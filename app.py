import streamlit as st

def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        st.success("Login bem-sucedido!")
    
    if st.button("Sign Up"):
        st.session_state.page = "Sign Up"

def cadastrar():
    st.title("Sign Up")
    new_username = st.text_input("Novo Usuário")
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")

    if len(new_username) < 3:
        st.error("O nome de usuário deve ter no mínimo 3 caracteres.")
    
    if len(new_password) < 6:
        st.error("A senha deve ter no mínimo 6 caracteres.")
    
    if new_password != confirm_password:
        st.error("As senhas não coincidem.")
    
    if len(new_username) >= 3 and len(new_password) >= 6 and st.button("Sign Up"):
        st.success("Nova conta cadastrada com sucesso!")
        st.session_state.page = "Login"
    
    if st.button("Login"):
        st.session_state.page = "Login"
        
def main():
    st.set_page_config(page_title='GADM')

    if "page" not in st.session_state:
        st.session_state.page = "Login"

    if st.session_state.page == "Login":
        login()
    elif st.session_state.page == "Sign Up":
        cadastrar()
        
if __name__ == "__main__":
    main()