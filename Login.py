import streamlit as st


user = "admin"
passw = "admin"

def login():
    st.title("Halaman Login")
    st.subheader("Silahkan Untuk Login Terlebih Dahulu")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type= "password")
    
    if st.button("Login ngab"):
        if username == user and password == passw :
            st.session_state["logged_in"] = True
            st.sidebar.success("Login berhasil!")
        else:
            st.sidebar.error("Username atau password salah.")            

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
