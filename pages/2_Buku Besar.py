import streamlit as st
import pandas as pd

# Inisialisasi DataFrame untuk masing-masing akun jika belum ada
if 'ledgers' not in st.session_state:
    st.session_state.ledgers = {f'Account {i}': pd.DataFrame(columns=['Date', 'Description', 'Debit', 'Credit']) for i in range(1, 16)}

st.title('Buku Besar')

# Form untuk menambahkan transaksi
st.header('Tambah Transaksi')
with st.form('transaction_form'):
    date = st.date_input('Tanggal')
    description = st.text_input('Deskripsi')

    account = st.selectbox('Pilih Akun', [f'Account {i}' for i in range(1, 16)])
    debit = st.number_input('Debit (Dalam Ribu Rupiah)', min_value=0.0, format="%.2f")
    credit = st.number_input('Kredit (Dalam Ribu Rupiah)', min_value=0.0, format="%.2f")
    submitted = st.form_submit_button('Tambahkan')

    if submitted:
        # Tambahkan transaksi ke akun yang dipilih
        new_transaction = pd.DataFrame({
            'Date': [date],
            'Description': [description],
            'Debit': [debit],
            'Credit': [credit]
        })
        st.session_state.ledgers[account] = pd.concat([st.session_state.ledgers[account], new_transaction], ignore_index=True)
        st.success(f'Transaksi berhasil ditambahkan ke {account}!')

# Tampilkan buku besar untuk setiap akun jika sudah ada data di session state
if st.session_state.get('ledgers'):
    st.header('Buku Besar Per Akun')
    for account, ledger in st.session_state.ledgers.items():
        st.subheader(account)
        if not ledger.empty:
            st.dataframe(ledger)

            # Pilih transaksi untuk dihapus
            st.subheader(f'Hapus Transaksi dari {account}')
            transaction_index = st.number_input(f'Masukkan nomor transaksi yang ingin dihapus dari {account}', min_value=0, max_value=len(ledger)-1, step=1, key=f'delete_{account}')
            delete_button = st.button(f'Hapus dari {account}', key=f'button_{account}')

            if delete_button:
                st.session_state.ledgers[account] = st.session_state.ledgers[account].drop(transaction_index).reset_index(drop=True)
                st.success(f'Transaksi berhasil dihapus dari {account}!')
        else:
            st.write(f'Belum ada transaksi di {account}.')
else:
    st.warning("Data buku besar tidak ditemukan. Silakan tambahkan transaksi.")