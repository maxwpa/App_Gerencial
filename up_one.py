import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

parcelas = list(range(1, 13))
parcelamento = st.selectbox("Número de Parcelas", parcelas)

data_pagamento = st.date_input('Data do Pagamento À Vista ou Primeira Parcela:', datetime.now().date())

hoje = datetime.now().date()

par_pagas = relativedelta(hoje, data_pagamento)

if hoje <= data_pagamento:
    parcelas_pagas = 0
else:
    parcelas_pagas = par_pagas.years * 12 + par_pagas.months + 1
    
parcelas_restantes = parcelamento - parcelas_pagas

st.write('parcelamento:', parcelamento)
st.write('data_pagamento:', data_pagamento)
st.write('hoje:', hoje)
st.write('par_pagas:', par_pagas)
st.write('parcalas_pagas:', parcelas_pagas)
st.write('parcelas_restantes:', parcelas_restantes)

if parcelas_restantes > 0:
    proxima_data = data_pagamento + relativedelta(months=parcelas_pagas)
    diferenca = proxima_data - hoje
    proxima_parcela = diferenca.days
else:
    proxima_data = 'QUITADO'
    proxima_parcela = 'QUITADO'

st.write('proxima_data:', proxima_data)
st.write('proxima_parcela:', proxima_parcela)

lista_datas_parcelas = []
for i in range(parcelamento):
    proxima_data = data_pagamento + relativedelta(months=(parcelas_pagas + i))
    lista_datas_parcelas.append(proxima_data)

st.write('lista_datas_parcelas:', lista_datas_parcelas)