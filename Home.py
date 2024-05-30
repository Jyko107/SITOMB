import streamlit as st
import requests
from PIL import Image
from streamlit_lottie import st_lottie
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(page_title="Sistem Informasi Soto Mie Bogor", page_icon=":🍲:", layout="wide")

user = "admin"
passw = "admin"

def login():
    st.title("Halaman Login")
    st.subheader("Silahkan Untuk Login Terlebih Dahulu")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type= "password")
    
    if st.button("Login"):
        if username == user and password == passw :
            st.session_state["logged_in"] = True
            st.sidebar.success("Login berhasil!")
        else:
            st.sidebar.error("Username atau password salah.")            

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()

if not st.session_state["logged_in"]:
    st.error("Anda harus login terlebih dahulu.")
else:   
    st.sidebar.success("Pilih Menu Diatas ini.")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

        st.experimental_rerun()
    #animate
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    #css
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    #ambil file css
    local_css("style/style.css")

    lottie_coading = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")


    #header
    with st.container():
        st.subheader("Selamat datang     di SITOMB:wave:")
        st.title("Sistem Informasi Soto Bogor - SITOMB")
        st.write('''''')


    #informasi
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Informasi Produk")
            st.write("##")
            st.write("""
                    Kami menjual soto mie bogor yang merupakan salah satu makanan khas Nusantara yang terbilang
                    soto lengkap karena terdapat banyak bahan-bahan yang disajikan dalam satu mangkoknya.
                    Hal unik yang kami sediakan dari  makanan berkuah ini adalah penyajiannya yang dilengkapi
                    dengan mi kuning, dan risol umumnya soto disajikan hanya menggunakan mi soun atau bihun.
                        """)

        with right_column:
            st_lottie(lottie_coading, height=300, key="coding")


    #foto
    Image1 = Image.open('images/sotodag.jpeg')
    Image2 = Image.open('images/soyam.jpeg')
    with st.container():
        st.write("---")
        st.header("Produk")
        st.write('##')
        left_column, right_column = st.columns(2)
        with left_column:
            st.image(Image1, caption="Soto Mie Bogor Daging", width=500)
            st.write('##')
            st.write(''' Soto Bogor Daging yang terbuat dari bahan - bahan
                    Mie Basah, Bihun, Kol, Daging Sapi, Tomat, Bumbu Paon,
                    Bawang Goreng, Daun Daunan.''')
        with right_column:
            st.image(Image2, caption="Soto Mie Bogor Ayam", width=425,)
            st.write('##')
            st.write(''' Soto Bogor Ayam yang terbuat dari bahan - bahan
                    Mie Basah, Bihun, Kol, Daging Ayam, Tomat, Bumbu Paon,
                    Bawang Goreng, Daun Daunan.''')
           
    st.write("##")
    st.write("---")

