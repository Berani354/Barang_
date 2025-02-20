import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import matplotlib.pyplot as plt

class Barang:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def info_barang(self):
        return f"Nama: {self.nama}, Harga: {self.harga} IDR, Stok: {self.stok}"

class Elektronik(Barang):
    def __init__(self, nama, harga, stok, merek, garansi):
        super().__init__(nama, harga, stok)
        self.merek = merek
        self.garansi = garansi

    def info_barang(self):
        return f"{super().info_barang()}, Merek: {self.merek}, Garansi: {self.garansi} tahun"

class Pakaian(Barang):
    def __init__(self, nama, harga, stok, ukuran, bahan):
        super().__init__(nama, harga, stok)
        self.ukuran = ukuran
        self.bahan = bahan

    def info_barang(self):
        return f"{super().info_barang()}, Ukuran: {self.ukuran}, Bahan: {self.bahan}"

class PeralatanSekolah(Barang):
    def __init__(self, nama, harga, stok, jenis, merek):
        super().__init__(nama, harga, stok)
        self.jenis = jenis
        self.merek = merek

    def info_barang(self):
        return f"{super().info_barang()}, Jenis: {self.jenis}, Merek: {self.merek}"

class Gudang:
    def __init__(self):
        self.daftar_barang = []
        self.load_from_excel()

    def tambah_barang(self, barang):
        self.daftar_barang.append(barang)
        self.save_to_excel()

    def cari_barang(self, nama):
        return next((barang for barang in self.daftar_barang if barang.nama.lower() == nama.lower()), None)

    def update_stok(self, nama, jumlah):
        barang = self.cari_barang(nama)
        if barang:
            barang.stok += jumlah
            self.save_to_excel()
            return True
        return False

    def hapus_barang(self, nama):
        barang = self.cari_barang(nama)
        if barang:
            self.daftar_barang.remove(barang)
            self.save_to_excel()
            return True
        return False

    def total_nilai_inventaris(self):
        return sum(barang.harga * barang.stok for barang in self.daftar_barang)

    def save_to_excel(self):
        data = []
        for barang in self.daftar_barang:
            row = [barang.nama, barang.harga, barang.stok, type(barang).__name__]
            row.extend([
                getattr(barang, 'merek', ''),
                getattr(barang, 'garansi', ''),
                getattr(barang, 'ukuran', ''),
                getattr(barang, 'bahan', ''),
                getattr(barang, 'jenis', '')
            ])
            data.append(row)
        
        pd.DataFrame(data, columns=['Nama', 'Harga', 'Stok', 'Kategori', 'Merek', 'Garansi', 'Ukuran', 'Bahan', 'Jenis']).to_excel('gudang.xlsx', index=False)

    def load_from_excel(self):
        if os.path.exists('gudang.xlsx'):
            df = pd.read_excel('gudang.xlsx')
            for _, row in df.iterrows():
                nama = row['Nama']
                harga = row['Harga']
                stok = row['Stok']
                kategori = row['Kategori']
                if kategori == 'Elektronik':
                    barang = Elektronik(nama, harga, stok, row['Merek'], row['Garansi'])
                elif kategori == 'Pakaian':
                    barang = Pakaian(nama, harga, stok, row['Ukuran'], row['Bahan'])
                elif kategori == 'PeralatanSekolah':
                    barang = PeralatanSekolah(nama, harga, stok, row['Jenis'], row['Merek'])
                else:
                    continue
                self.daftar_barang.append(barang)

warehouse = Gudang()

class BarangUI:
    def __init__(self, warehouse):
        self.warehouse = warehouse

    def tambah_barang(self):
        st.title("Tambah Barang")
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga", min_value=0)
        stok = st.number_input("Stok", min_value=0)
        kategori = st.selectbox("Kategori", ["Elektronik", "Pakaian", "Peralatan Sekolah"])
        if kategori == "Elektronik":
            merek = st.text_input("Merek")
            garansi = st.number_input("Garansi (tahun)", min_value=0)
            if st.button("Tambah Elektronik"):
                barang = Elektronik(nama, harga, stok, merek, garansi)
                self.warehouse.tambah_barang(barang)
                st.success("Barang elektronik berhasil ditambahkan", icon="📦")
        elif kategori == "Pakaian":
            ukuran = st.text_input("Ukuran")
            bahan = st.text_input("Bahan")
            if st.button("Tambah Pakaian"):
                barang = Pakaian(nama, harga, stok, ukuran, bahan)
                self.warehouse.tambah_barang(barang)
                st.success("Barang pakaian berhasil ditambahkan", icon="👕")
        elif kategori == "Peralatan Sekolah":
            jenis = st.text_input("Jenis")
            merek = st.text_input("Merek")
            if st.button("Tambah Peralatan Sekolah"):
                barang = PeralatanSekolah(nama, harga, stok, jenis, merek)
                self.warehouse.tambah_barang(barang)
                st.success("Peralatan sekolah berhasil ditambahkan", icon="📚")

    def tampilkan_barang(self):
        st.title("Daftar Barang")
        if self.warehouse.daftar_barang:
            elektronik = [barang for barang in self.warehouse.daftar_barang if isinstance(barang, Elektronik)]
            pakaian = [barang for barang in self.warehouse.daftar_barang if isinstance(barang, Pakaian)]
            peralatan_sekolah = [barang for barang in self.warehouse.daftar_barang if isinstance(barang, PeralatanSekolah)]
            st.header("Elektronik")
            st.table(pd.DataFrame([[barang.nama, barang.harga, barang.stok, barang.merek, barang.garansi] for barang in elektronik], columns=["Nama", "Harga", "Stok", "Merek", "Garansi"]))
            st.header("Pakaian")
            st.table(pd.DataFrame([[barang.nama, barang.harga, barang.stok, barang.ukuran, barang.bahan] for barang in pakaian], columns=["Nama", "Harga", "Stok", "Ukuran", "Bahan"]))
            st.header("Peralatan Sekolah")
            st.table(pd.DataFrame([[barang.nama, barang.harga, barang.stok, barang.jenis, barang.merek] for barang in peralatan_sekolah], columns=["Nama", "Harga", "Stok", "Jenis", "Merek"]))
            fig, ax = plt.subplots()
            ax.pie([len(elektronik), len(pakaian), len(peralatan_sekolah)], labels=["Elektronik", "Pakaian", "Peralatan Sekolah"], autopct='%1.1f%%', startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.write("Gudang kosong")        
    def cari_barang(self):
        st.title("Cari Barang")
        nama = st.text_input("Nama Barang")
        if st.button("Cari"):
            barang = self.warehouse.cari_barang(nama)
            if barang:
                st.write(barang.info_barang())
            else:
                st.write("Barang tidak ditemukan")

    def update_stok(self):
        st.title("Update Stok Barang")

        # Display all items initially
        data = [[barang.nama, barang.harga, barang.stok, type(barang).__name__,
                 getattr(barang, 'merek', ''), getattr(barang, 'garansi', ''),
                 getattr(barang, 'ukuran', ''), getattr(barang, 'bahan', ''),
                 getattr(barang, 'jenis', '')] for barang in self.warehouse.daftar_barang]
        df = pd.DataFrame(data, columns=["Nama", "Harga", "Stok", "Kategori", "Merek", "Garansi", "Ukuran", "Bahan", "Jenis"])

        # Display the items in a table
        st.dataframe(df)

        # Check if there are any items in the list
        if not df.empty:
            # Select a barang to update
            nama = st.selectbox("Pilih Barang untuk Update Stok", df["Nama"].tolist())
            jumlah = st.number_input("Jumlah Penambahan", min_value=0)
            if st.button("Update Stok"):
                if self.warehouse.update_stok(nama, jumlah):
                    st.success(f"Stok {nama} berhasil diperbarui")
                else:
                    st.error("Barang tidak ditemukan")
        else:
            st.write("Tidak ada barang yang ditemukan")


    def hapus_barang(self):
        st.title("Hapus Barang")
        nama = st.text_input("Nama Barang")
        if st.button("Hapus"):
            if self.warehouse.hapus_barang(nama):
                st.success("Barang berhasil dihapus")
            else:
                st.error("Barang tidak ditemukan")
                
    def total_nilai_inventaris(self):
        st.title("Total Nilai Inventaris")
        total = self.warehouse.total_nilai_inventaris()
        formatted_total = "Rp {:,.2f}".format(total)
        st.write(f"Total Nilai Inventaris: {formatted_total}")

# Create an instance of BarangUI
barang_ui = BarangUI(warehouse)

# Streamlit option menu for navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Tambah Barang", "Tampilkan Barang", "Cari Barang", "Update Stok Barang", "Hapus Barang", "Total Nilai Inventaris"],
        icons=["plus", "list", "search", "upload", "trash", "wallet"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Tambah Barang":
    barang_ui.tambah_barang()
elif selected == "Tampilkan Barang":
    barang_ui.tampilkan_barang()
elif selected == "Cari Barang":
    barang_ui.cari_barang()
elif selected == "Update Stok Barang":
    barang_ui.update_stok()
elif selected == "Hapus Barang":
    barang_ui.hapus_barang()
elif selected == "Total Nilai Inventaris":
    barang_ui.total_nilai_inventaris()
