import streamlit as st

def acesso():
 
    st.set_page_config(
        page_title="SGN - Sistema de Gerenciamento de Negócios",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="title-container">
            <h1>Bem-vindo ao SGN</h1>
            <h10>Sistema de Gerenciamento de Negócios</h10>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cubiodesign.com/kalium/wp-content/uploads/2017/09/data-analytics-logo.jpg", width=150)

        st.markdown(
        """
        <div style="">
            <style>
                img {
                    border-radius: 5px;
                    display: block;
                    margin-left: 60px;
                    margin-top: 20px;
            </style>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        st.markdown(
            """
            <div style="">
                <style>
                    .stTextInput label {
                        color: white;
                        font-weight: bold;
                    }
                </style>
            </div>
                """,
                unsafe_allow_html=True
            )
        codigo_de_acesso = st.text_input('Código de Acesso', type='password')
        
        st.markdown(
            """
            <style>
                .stButton button {
                    background-color: green;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        entrar = st.button('Entrar')

    if codigo_de_acesso == "2" and entrar:
        st.session_state.logged_in = True
    elif entrar:
        st.warning("Código de acesso incorreto. Tente novamente.")
        
    back_image = "https://www.10wallpaper.com/wallpaper/1680x1050/1411/Cool_Black_3D-Abstract_widescreen_wallpaper_1680x1050.jpg"
    page_bg_img = f'''
        <style>
            .stApp {{
                background-image: url("{back_image}");
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        <script>
            document.body.style.zoom = 3.8;
        </script>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

if __name__ == "__main__":
    acesso()