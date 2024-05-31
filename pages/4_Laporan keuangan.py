import streamlit as st
import pandas as pd

def main():
    st.title("Laporan Keuangan")

    # Sidebar untuk input data
    st.header("Input Data")
    tgl_laporan = st.date_input("Tanggal Laporan:")
    
    st.subheader("Laporan Laba Rugi")
    pendapatan_usaha = st.number_input("Pendapatan Usaha:", value=0)
    biaya_bahan_baku = st.number_input("Biaya Bahan Baku:", value=0)
    biaya_tenaga_kerja = st.number_input("Biaya Tenaga Kerja:", value=0)
    biaya_overhead_pabrik = st.number_input("Biaya Overhead Pabrik:", value=0)
    biaya_operasional = st.number_input("Biaya Operasional:", value=0)
    
    st.subheader("Laporan Perubahan Modal")
    modal_awal = st.number_input("Modal Awal:", value=0)
    
    st.subheader("Laporan Posisi Keuangan")
    kas = st.number_input("Kas:", value=0)
    piutang_usaha = st.number_input("Piutang Usaha:", value=0)
    
    st.subheader("Total Kewajiban dan Modal")
    hutang_usaha = st.number_input("Hutang Usaha:", value=0)
    
    laba_bersih = pendapatan_usaha - (biaya_bahan_baku + biaya_tenaga_kerja + biaya_overhead_pabrik + biaya_operasional)
    total_modal = modal_awal + laba_bersih
    total_aset = kas + piutang_usaha
    total_kewajiban_modal = total_modal + hutang_usaha
  # Menampilkan laporan laba rugi
    st.header("Laporan Laba Rugi")
    st.write("Pendapatan Usaha:", pendapatan_usaha)
    st.write("Biaya Bahan Baku:", biaya_bahan_baku)
    st.write("Biaya Tenaga Kerja:", biaya_tenaga_kerja)
    st.write("Biaya Overhead Pabrik:", biaya_overhead_pabrik)
    st.write("Biaya Operasional:", biaya_operasional)
    st.write("Laba Bersih:", laba_bersih)

    # Menampilkan laporan perubahan modal
    st.header("Laporan Perubahan Modal")
    st.write("Modal Awal:", modal_awal)
    st.write("Laba Bersih Tahun Berjalan:", laba_bersih)
    st.write("Total Modal:", total_modal)

    # Menampilkan laporan posisi keuangan
    st.header("Laporan Posisi Keuangan")
    st.write("Kas:", kas)
    st.write("Piutang Usaha:", piutang_usaha)
    st.write("Total Aset:", total_aset)
    st.write("Hutang Usaha:", hutang_usaha)
    st.write("Total Kewajiban dan Modal:", total_kewajiban_modal)

    # Memungkinkan pengguna mengunduh data ke dalam format CSV
    data = {
        'Tanggal Laporan': [tgl_laporan],
        'Pendapatan Usaha': [pendapatan_usaha],
        'Biaya Bahan Baku': [biaya_bahan_baku],
        'Biaya Tenaga Kerja': [biaya_tenaga_kerja],
        'Biaya Overhead Pabrik': [biaya_overhead_pabrik],
        'Biaya Operasional': [biaya_operasional],
        'Modal Awal': [modal_awal],
        'Laba Bersih': [laba_bersih],
        'Kas': [kas],
        'Piutang Usaha': [piutang_usaha],
        'Hutang Usaha': [hutang_usaha],
        'Total Kewajiban dan Modal': [total_kewajiban_modal]
 }

if __name__== "__main__":
    main()
