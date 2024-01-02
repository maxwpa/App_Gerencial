import streamlit as st

def login():
    st.title('Login')
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')
    st.button('Entrar')
    
def sign_up():
    st.title('Sign Up')
    new_username = st.text_input('Novo Usuário')
    new_password = st.text_input('Inserir Senha', type='password')
    cfm_password = st.text_input('Confirmar Senha', type='password')
    new_login = st.button('Novo Login')
    if new_login and len(new_username) <= 2:
        st.error('O nome de usuário deve ter no mínimo 3 caracteres')
    if new_login and len(new_password) <= 5:
        st.error('A senha deve conter no mínimo 6 caracteres')
    if new_login and new_password != cfm_password:
        st.error('As senhas não coincidem')

def main():
    st.set_page_config(page_title='GDMA')
    col_one, col_two = st.columns(2)
    with col_one:
        login()
    with col_two:
        sign_up()
        
if __name__ == "__main__":
    main()
