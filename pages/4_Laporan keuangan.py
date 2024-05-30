import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

st.title('Laporan Keuangan')

# Connect to SQLite database
conn = sqlite3.connect('Laporan Keuangan.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (Tanggal TEXT, Keterangan TEXT, Debit REAL, Kredit REAL)''')
conn.commit()

def form():
    st.write("Isi Data Transaksi")
    with st.form(key="transaction_form"):
        Tanggal = st.date_input("Tanggal:")
        Keterangan = st.text_input("Keterangan:")
        Debit = st.number_input("Debit (Dalam Ribu Rupiah):", min_value=0.0, format="%.2f")
        Kredit = st.number_input("Kredit (Dalam Ribu Rupiah):", min_value=0.0, format="%.2f")
        submission = st.form_submit_button(label="Submit")
        
        if submission:
            c.execute("INSERT INTO transactions (Tanggal, Keterangan, Debit, Kredit) VALUES (?, ?, ?, ?)", 
                      (Tanggal, Keterangan, Debit, Kredit))
            conn.commit()
            st.success("Transaksi berhasil disubmit")

def display_data():
    st.write("Data Transaksi")
    c.execute("SELECT * FROM transactions")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Tanggal', 'Keterangan', 'Debit', 'Kredit'])
    st.write(df)

def delete_data():
    row_to_delete = st.text_input("Masukkan nomor baris yang akan dihapus:")
    if st.button("Delete"):
        c.execute("DELETE FROM transactions WHERE rowid=?", (row_to_delete,))
        conn.commit()
        st.success("Baris berhasil dihapus")

def laporan_laba_rugi():
    st.header("Laporan Laba Rugi")
    c.execute("SELECT Keterangan, SUM(Debit) - SUM(Kredit) as Amount FROM transactions GROUP BY Keterangan")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Keterangan', 'Amount'])
    st.write(df)

def laporan_perubahan_modal():
    st.header("Laporan Perubahan Modal")
    initial_capital = st.number_input("Modal Awal (Dalam Ribu Rupiah):", min_value=0.0, format="%.2f")
    c.execute("SELECT SUM(Debit) - SUM(Kredit) FROM transactions WHERE Keterangan LIKE 'Modal%'")
    capital_changes = c.fetchone()[0] or 0.0
    final_capital = initial_capital + capital_changes
    st.write(f"Modal Awal: {initial_capital} Ribu Rupiah")
    st.write(f"Perubahan Modal: {capital_changes} Ribu Rupiah")
    st.write(f"Modal Akhir: {final_capital} Ribu Rupiah")

def laporan_posisi_keuangan():
    st.header("Laporan Posisi Keuangan")
    c.execute("SELECT SUM(Debit) FROM transactions")
    total_debit = c.fetchone()[0] or 0.0
    c.execute("SELECT SUM(Kredit) FROM transactions")
    total_kredit = c.fetchone()[0] or 0.0
    st.write(f"Total Aset: {total_debit} Ribu Rupiah")
    st.write(f"Total Kewajiban: {total_kredit} Ribu Rupiah")
    st.write(f"Ekuitas: {total_debit - total_kredit} Ribu Rupiah")

# Display forms and reports
form()
display_data()
delete_data()
laporan_laba_rugi()
laporan_perubahan_modal()
laporan_posisi_keuangan()

# Close the database connection
conn.close()