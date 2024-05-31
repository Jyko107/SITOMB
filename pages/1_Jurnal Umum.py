import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

# Title of the app
st.title('Jurnal Umum')

# Connect to SQLite database
conn = sqlite3.connect('Jurnal_Umum55.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS information
             (Tanggal TEXT, Account TEXT, Debit REAL, Kredit REAL)''')
conn.commit()

def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def form():
    st.write("Isi Data Transaksi")
    with st.form(key="information_form"):
        Tanggal = st.date_input("Tanggal:", date.today())
        Debit_Account = st.text_input("Akun Debit:")
        Debit = st.text_input("Jumlah Debit (dalam Rupiah):")
        Kredit_Account = st.text_input("Akun Kredit:")
        Kredit = st.text_input("Jumlah Kredit (dalam Rupiah):")
        submission = st.form_submit_button(label="Submit")

    if submission:
        Debit = float(Debit.replace(".", "").replace(",", ".")) if Debit else 0.0
        Kredit = float(Kredit.replace(".", "").replace(",", ".")) if Kredit else 0.0

        try:
            Debit = float(Debit)
            Kredit = float(Kredit)
            if Debit != Kredit:
                st.error("Jumlah Debit dan Kredit harus sama!")
            else:
                # Insert debit entry
                c.execute("INSERT INTO information (Tanggal, Account, Debit, Kredit) VALUES (?, ?, ?, ?)", 
                          (Tanggal, Debit_Account, Debit, 0))
                # Insert credit entry
                c.execute("INSERT INTO information (Tanggal, Account, Debit, Kredit) VALUES (?, ?, ?, ?)", 
                          (Tanggal, Kredit_Account, 0, Kredit))
                conn.commit()
                st.success("Transaksi berhasil disimpan!")
        except ValueError:
            st.error("Jumlah Debit dan Kredit harus berupa angka!")

def display_data():
    c.execute("SELECT rowid, * FROM information")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['RowID', 'Tanggal', 'Akun', 'Debit', 'Kredit'])
    st.write(df)

def calculate_saldo():
    c.execute("SELECT SUM(Debit), SUM(Kredit) FROM information")
    saldo = c.fetchone()
    total_debit = saldo[0] if saldo[0] is not None else 0.0
    total_kredit = saldo[1] if saldo[1] is not None else 0.0
    st.write(f"Total Debit: {format_rupiah(total_debit)}")
    st.write(f"Total Kredit: {format_rupiah(total_kredit)}")
   
def delete_data():
    row_to_delete = st.text_input("Masukkan nomor baris yang ingin dihapus:")
    if st.button("Hapus"):
        try:
            row_to_delete = int(row_to_delete)
            c.execute("DELETE FROM information WHERE rowid=?", (row_to_delete,))
            conn.commit()
            if c.rowcount > 0:
                st.success("Baris berhasil dihapus!")
            else:
                st.error("Nomor baris tidak ditemukan.")
        except ValueError:
            st.error("Masukkan nomor baris yang valid.")



# Run the functions
form()
display_data()
calculate_saldo()
delete_data()

# Close the database connection
conn.close()
