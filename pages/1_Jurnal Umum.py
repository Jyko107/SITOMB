import streamlit as st
import sqlite3
from datetime import date
import pandas as pd





st.title('Jurnal Umum')
st.sidebar.success("Pilih Menu Diatas ini.")

conn = sqlite3.connect('Jurnal_Umum0.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS information
             (Tanggal TEXT, Keterangan1 TEXT, Debit REAL, Keterangan2 TEXT, Kredit REAL)''')
conn.commit()

def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def form():
    st.write("Isi Data Transaksi")
    with st.form(key="information_form"):
        Tanggal = st.date_input("Tanggal:", value=date.today())
        Keterangan1 = st.text_input("Keterangan 1:")
        Debit = st.number_input("Debit (Dalam Ribu Rupiah):", min_value=0.0, step=1000.0)
        Keterangan2 = st.text_input("Keterangan 2:")
        Kredit = st.number_input("Kredit (Dalam Ribu Rupiah):", min_value=0.0, step=1000.0)
        submission = st.form_submit_button(label="Submit")
    if submission:
        c.execute("INSERT INTO information (Tanggal, Keterangan1, Debit, Keterangan2, Kredit) VALUES (?, ?, ?, ?, ?)", (Tanggal, Keterangan1, Debit, Keterangan2, Kredit))
        conn.commit()
        st.success("Successfully submitted")

def display_data():
    c.execute("SELECT rowid, * FROM information")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['RowID', 'Tanggal', 'Keterangan 1', 'Debit', 'Keterangan 2', 'Kredit'])
    df['Debit'] = df['Debit'].apply(format_rupiah)
    df['Kredit'] = df['Kredit'].apply(format_rupiah)
    st.write(df)

def calculate_saldo():
    c.execute("SELECT SUM(Debit), SUM(Kredit) FROM information")
    saldo = c.fetchone()
    total_debit = saldo[0] if saldo[0] is not None else 0.0
    total_kredit = saldo[1] if saldo[1] is not None else 0.0
    st.header(f"Total Debit: {format_rupiah(total_debit)}")
    st.header(f"Total Kredit: {format_rupiah(total_kredit)}")
    st.header(f"Saldo: {format_rupiah(total_debit - total_kredit)}")

def delete_data():
    row_to_delete = st.text_input("Enter the row number to delete:")
    if st.button("Delete"):
        c.execute("DELETE FROM information WHERE rowid=?", (row_to_delete,))
        conn.commit()
        st.success("Row deleted successfully")

def edit_data():
    st.write("Edit Data")
    row_to_edit = st.text_input("Enter the row number to edit:")
    if row_to_edit:
        c.execute("SELECT * FROM information WHERE rowid=?", (row_to_edit,))
        data = c.fetchone()
        if data:
            Tanggal, Keterangan1, Debit, Keterangan2, Kredit = data
            new_Tanggal = st.date_input("Tanggal:", value=pd.to_datetime(Tanggal))
            new_Keterangan1 = st.text_input("Keterangan 1:", value=Keterangan1)
            new_Debit = st.number_input("Debit (Dalam Ribu Rupiah):", min_value=0.0, step=1000.0, value=Debit)
            new_Keterangan2 = st.text_input("Keterangan 2:", value=Keterangan2)
            new_Kredit = st.number_input("Kredit (Dalam Ribu Rupiah):", min_value=0.0, step=1000.0, value=Kredit)
            if st.button("Update"):
                c.execute("UPDATE information SET Tanggal=?, Keterangan1=?, Debit=?, Keterangan2=?, Kredit=? WHERE rowid=?", 
                          (new_Tanggal, new_Keterangan1, new_Debit, new_Keterangan2, new_Kredit, row_to_edit))
                conn.commit()
                st.success("Row updated successfully")
form()
display_data()
calculate_saldo()
delete_data()
edit_data()
conn.close()
