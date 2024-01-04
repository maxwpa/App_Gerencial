import streamlit as st
import sqlite3

conn = sqlite3.connect('dados_registradas.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS novos_produtos (id INTEGER PRIMARY KEY, produto TEXT, modelo TEXT)')
cursor.execute('SELECT produto FROM novos_produtos')
prod_opc = [row[0] for row in cursor.fetchall()]

prod_opc.append('Novo Produto')

prod = st.selectbox('Produto comprado:', prod_opc)

cursor.execute('SELECT modelo FROM novos_produtos')
model_opc = [row[0] for row in cursor.fetchall()]

model_opc.append('Novo Modelo')

model = st.selectbox('Modelo:', model_opc)

def registrar_produto():
   
    if prod == 'Novo Produto':
        new_prod = st.text_input('Cadastre novo produto:')
        produto = new_prod
        if new_prod not in prod_opc:
            cursor.execute('INSERT INTO novos_produtos (produto) VALUES (?)', (new_prod,))
            conn.commit()
    else:
        produto = prod

   
    if model == 'Novo Modelo':
        new_model = st.text_input('Cadastre novo modelo:')
        modelo = new_model
        if new_model not in model_opc:
            cursor.execute('INSERT INTO novos_produtos (modelo) VALUES (?)', (new_model,))
            conn.commit()
    else:
        modelo = model
    registrar = st.button('Registrar')

cursor.close()
conn.close()
