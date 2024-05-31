import streamlit as st
import sqlite3
from datetime import date
import pandas as pd


st.title('Transaksi')

conn = sqlite3.connect('Transaksion.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS information
             (Tanggal Text, Keterangan Text, qty Text, Harga Integer)''')
conn.commit()

def format_rupiah(amount):
    return f"Rp {int(amount):,}".replace(",", ".")

def form():
    st.write("Isi Data Transaksi")
    with st.form(key="information form"):
        Tanggal = st.date_input("Tanggal:")
        Keterangan = st.text_input("Keterangan:")
        qty = st.text_input("Jumlah:")
        Harga_input = st.text_input("Harga (dalam Rupiah):")
        
        submission = st.form_submit_button(label="Submit")
        
        if submission:
            # Remove dots and convert to integer
            try:
                Harga = int(Harga_input.replace(".", ""))
                c.execute("INSERT INTO information (Tanggal, Keterangan, qty, Harga) VALUES (?, ?, ?, ?)", (Tanggal, Keterangan, qty, Harga))
                conn.commit()
                st.success("Successfully submitted")
            except ValueError:
                st.error("Harga")

def display_data():
    c.execute("SELECT * FROM information")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Tanggal', 'Keterangan', 'qty', 'Harga'])
    # Format Harga column
    df['Harga'] = df['Harga'].apply(format_rupiah)
    st.write(df)

def calculate_saldo():
    c.execute("SELECT SUM(Harga) FROM information")
    saldo = c.fetchone()[0]
    if saldo is None:
        saldo = 0
    st.header(f"Saldo: {format_rupiah(saldo)}")

def delete_data():
    row_to_delete = st.text_input("Masukkan nomor baris yang akan dihapus:")
    if st.button("Delete"):
        c.execute("DELETE FROM information WHERE rowid=?", (row_to_delete,))
        conn.commit()
        st.success("Baris berhasil dihapus")

form()
display_data()
calculate_saldo()
delete_data()
conn.close()
