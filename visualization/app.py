import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Path file data
DATA_PATH = '/home/alrahma/Proyek-Pemrograman/airflow/data/processed_data.csv'

# Fungsi untuk memuat data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # Jika file belum ada, buat file kosong
        df = pd.DataFrame(columns=['Tanggal', 'Uang Masuk', 'Uang Keluar', 'Saldo Kumulatif'])
        df.to_csv(path, index=False)
        return df

# Fungsi untuk menyimpan data baru
def save_data(new_data, path):
    df = load_data(path)
    df = pd.concat([df, new_data], ignore_index=True)
    # Hitung saldo kumulatif
    df['Saldo Kumulatif'] = df['Uang Masuk'].cumsum() - df['Uang Keluar'].cumsum()
    df.to_csv(path, index=False)

# Fungsi format rupiah
def format_rupiah(value):
    return f"Rp {value:,.2f}".replace(",", ".").replace(".00", "").replace(".", ",")

# Memuat data
df = load_data(DATA_PATH)

# Menghitung total pemasukan, pengeluaran, dan saldo saat ini
total_pemasukan = df['Uang Masuk'].sum()
total_pengeluaran = df['Uang Keluar'].sum()
saldo_akhir = total_pemasukan - total_pengeluaran

# Halaman utama
st.title('Dashboard Keuangan Harian')

# Menampilkan ringkasan saldo, pemasukan, dan pengeluaran
st.write("## **Ringkasan Keuangan**")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="**Saldo Saat Ini**", value=format_rupiah(saldo_akhir))
with col2:
    st.metric(label="**Total Pemasukan**", value=format_rupiah(total_pemasukan))
with col3:
    st.metric(label="**Total Pengeluaran**", value=format_rupiah(total_pengeluaran))

# Input Data Baru
st.sidebar.header('Tambah Data Transaksi')
with st.sidebar.form('input_form'):
    tanggal = st.date_input('Tanggal')
    uang_masuk = st.number_input('Uang Masuk', min_value=0.0, step=1.0)
    uang_keluar = st.number_input('Uang Keluar', min_value=0.0, step=1.0)
    submit = st.form_submit_button('Simpan Data')
    
    if submit:
        new_data = pd.DataFrame({
            'Tanggal': [tanggal],
            'Uang Masuk': [uang_masuk],
            'Uang Keluar': [uang_keluar]
        })
        save_data(new_data, DATA_PATH)
        st.success('Data berhasil disimpan! Silakan refresh halaman secara manual.')

        # Refresh halaman untuk menampilkan data baru
        st.experimental_rerun()

# Tampilkan data tabel
st.write("### **Data Transaksi Harian**")
st.dataframe(df)

st.write("### Grafik Pemasukan Harian")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df, x='Tanggal', y='Uang Masuk', ax=ax1, marker='o', color='green', label='Uang Masuk', linewidth=2)
ax1.fill_between(df['Tanggal'], df['Uang Masuk'], color='green', alpha=0.2)  # Area bawah grafik
ax1.set_title('Grafik Pemasukan Harian', fontsize=16, weight='bold')
ax1.set_xlabel('Tanggal', fontsize=12)
ax1.set_ylabel('Jumlah Uang Masuk', fontsize=12)
ax1.grid(alpha=0.3, linestyle='--')
ax1.legend()
st.pyplot(fig1)

# Grafik Pengeluaran
st.write("### Grafik Pengeluaran Harian")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df, x='Tanggal', y='Uang Keluar', ax=ax2, marker='o', color='blue', label='Uang Keluar', linewidth=2)
ax2.fill_between(df['Tanggal'], df['Uang Keluar'], color='blue', alpha=0.2)  # Area bawah grafik
ax2.set_title('Grafik Pengeluaran Harian', fontsize=16, weight='bold')
ax2.set_xlabel('Tanggal', fontsize=12)
ax2.set_ylabel('Jumlah Uang Keluar', fontsize=12)
ax2.grid(alpha=0.3, linestyle='--')
ax2.legend()
st.pyplot(fig2)

# Menambahkan copyright di bagian bawah
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; font-size: 12px; color: gray;">
        © 2024 Dashboard Keuangan Harian. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)

