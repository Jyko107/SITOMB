import streamlit as st
import pandas as pd

# Cek apakah data buku besar sudah ada
if 'ledgers' not in st.session_state:
    st.warning("Data buku besar tidak ditemukan. Silakan tambahkan transaksi di halaman Buku Besar.")
else:
    st.title('Neraca Saldo')

    # Perhitungan saldo akhir per akun dan pembentukan neraca saldo
    balances = {'Account': [], 'Debit (Dalam Ribu Rupiah)': [], 'Credit (Dalam Ribu Rupiah)': []}

    for account, ledger in st.session_state.ledgers.items():
        total_debit = ledger['Debit'].sum()
        total_credit = ledger['Credit'].sum()
        balance = total_debit - total_credit

        balances['Account'].append(account)
        if balance >= 0:
            balances['Debit (Dalam Ribu Rupiah)'].append(balance)
            balances['Credit (Dalam Ribu Rupiah)'].append(0.0)
        else:
            balances['Debit (Dalam Ribu Rupiah)'].append(0.0)
            balances['Credit (Dalam Ribu Rupiah)'].append(abs(balance))

    # Tampilkan neraca saldo
    balance_df = pd.DataFrame(balances)
    st.dataframe(balance_df)

    # Tampilkan total debit dan kredit
    total_debit = balance_df['Debit (Dalam Ribu Rupiah)'].sum()
    total_credit = balance_df['Credit (Dalam Ribu Rupiah)'].sum()

    st.subheader('Total')
    st.write(f'Total Debit: Rp {total_debit}')
    st.write(f'Total Kredit: Rp {total_credit}')