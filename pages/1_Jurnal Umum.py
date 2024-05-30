import streamlit as st
import sqlite3
from datetime import date
import pandas as pd


st.title('Jurnal Umum')

conn = sqlite3.connect('Jurnal Umum.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS information
             (Tanggal Text, Keterangan Text, Debit Text, Kredit Text )''')
conn.commit()

def form():
    st.write("Isi Data Transaksi")
    with st.form(key="information form"):
        Tanggal = st.date_input(" Tanggal : ")
        Keterangan = st.text_input(" keterangan : ")
        Debit = st.number_input(" Debit(Dalam Ribu Rupiah): ")
        Kredit = st.number_input( 'kredit (Dalam Ribu Rupiah): ')
        submission = st.form_submit_button(label ="Submit")
    if submission:
        c.execute("INSERT INTO information (Tanggal, Keterangan, Debit, Kredit) VALUES (?, ?, ?, ?)", (Tanggal, Keterangan, Debit, Kredit))
        conn.commit()
        st.success("Successfully submitted")
def display_data():
    c.execute("SELECT * FROM information")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Tanggal', 'Keterangan', 'Debit', 'Kredit'])
    st.write(df)

def delete_data():
    row_to_delete = st.text_input("Enter the row number to delete : ")
    if st.button("Delete"):
        c.execute("DELETE FROM information WHERE rowid=?", (row_to_delete,))
        conn.commit()
        st.success("Row deleted successfully")

form()
display_data()
delete_data()
conn.close()


