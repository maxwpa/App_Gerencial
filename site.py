import streamlit as st

def login():
    st.title('Login')
    st.text_input('Usuário')
    st.text_input('Senha', type='password')
    
def sign_up():
    st.title('Sign Up')
    st.text_input('Novo Usuário')
    st.text_input('Senha', type='password')
    st.text_input('Confirmar Senha', type='password')

sign_up()
