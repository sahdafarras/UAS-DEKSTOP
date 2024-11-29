import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Membuat atau menghubungkan ke database SQLite
conn = sqlite3.connect('kpop_store.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS merchandise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kategori TEXT NOT NULL,
    harga INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
""")
conn.commit()

# Fungsi Tambah Data
def tambah_data():
    nama = entry_nama.get()
    kategori = entry_kategori.get()
    harga = entry_harga.get()
    stok = entry_stok.get()
    
    if nama and kategori and harga and stok:
        cursor.execute("INSERT INTO merchandise (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)",
                       (nama, kategori, int(harga), int(stok)))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        reset_form()
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")

# Fungsi Tampilkan Data
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM merchandise")
    for data in cursor.fetchall():
        tree.insert("", "end", values=data)

# Fungsi Hapus Data
def hapus_data():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        id_data = item['values'][0]
        cursor.execute("DELETE FROM merchandise WHERE id = ?", (id_data,))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    else:
        messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")

# Fungsi Ubah Data
def ubah_data():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        id_data = item['values'][0]
        
        # Mendapatkan data baru dari form
        nama = entry_nama.get()
        kategori = entry_kategori.get()
        harga = entry_harga.get()
        stok = entry_stok.get()
        
        if nama and kategori and harga and stok:
            cursor.execute("""
                UPDATE merchandise 
                SET nama = ?, kategori = ?, harga = ?, stok = ?
                WHERE id = ?
            """, (nama, kategori, int(harga), int(stok), id_data))
            conn.commit()
            tampilkan_data()
            messagebox.showinfo("Sukses", "Data berhasil diubah!")
            reset_form()
        else:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
    else:
        messagebox.showwarning("Peringatan", "Pilih data yang akan diubah!")

# Fungsi Auto-Fill Form
def auto_fill_form(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        data = item['values']
        entry_nama.delete(0, END)
        entry_kategori.delete(0, END)
        entry_harga.delete(0, END)
        entry_stok.delete(0, END)
        entry_nama.insert(0, data[1])
        entry_kategori.insert(0, data[2])
        entry_harga.insert(0, data[3])
        entry_stok.insert(0, data[4])

# Fungsi Reset Form
def reset_form():
    entry_nama.delete(0, END)
    entry_kategori.delete(0, END)
    entry_harga.delete(0, END)
    entry_stok.delete(0, END)

# Fungsi Cari Produk
def cari_produk():
    keyword = entry_cari.get()
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM merchandise WHERE nama LIKE ?", (f"%{keyword}%",))
    for data in cursor.fetchall():
        tree.insert("", "end", values=data)

# GUI menggunakan Tkinter
root = Tk()
root.title("K-Pop Store Management")
root.geometry("1000x700")
root.configure(bg="#DCEEFF")

# Header
header = Frame(root, bg="#0052CC", pady=10)
header.pack(fill=X)
Label(header, text="K-Pop Store Management", bg="#0052CC", fg="white", font=("Arial", 16, "bold")).pack()

# Form Input
frame_form = Frame(root, bg="#DCEEFF", padx=10, pady=10)
frame_form.pack()

Label(frame_form, text="Nama Merchandise", bg="#DCEEFF", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
Label(frame_form, text="Kategori", bg="#DCEEFF", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
Label(frame_form, text="Harga", bg="#DCEEFF", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
Label(frame_form, text="Stok", bg="#DCEEFF", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)

entry_nama = Entry(frame_form, width=30)
entry_kategori = Entry(frame_form, width=30)
entry_harga = Entry(frame_form, width=30)
entry_stok = Entry(frame_form, width=30)

entry_nama.grid(row=0, column=1, pady=5)
entry_kategori.grid(row=1, column=1, pady=5)
entry_harga.grid(row=2, column=1, pady=5)
entry_stok.grid(row=3, column=1, pady=5)

Button(frame_form, text="Tambah Data", command=tambah_data, bg="#007BFF", fg="white", width=15).grid(row=4, column=0, pady=10)
Button(frame_form, text="Reset Form", command=reset_form, bg="#F44336", fg="white", width=15).grid(row=4, column=1, pady=10)
Button(frame_form, text="Ubah Produk", command=ubah_data, bg="#FFC107", fg="black", width=15).grid(row=5, column=0, pady=10)

# Tabel Merchandise
frame_table = Frame(root, bg="#DCEEFF", padx=10, pady=10)
frame_table.pack()

tree = ttk.Treeview(frame_table, columns=("ID", "Nama", "Kategori", "Harga", "Stok"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama Merchandise")
tree.heading("Kategori", text="Kategori")
tree.heading("Harga", text="Harga")
tree.heading("Stok", text="Stok")
tree.column("ID", width=50, anchor=CENTER)
tree.column("Nama", width=200)
tree.column("Kategori", width=150)
tree.column("Harga", width=100, anchor=CENTER)
tree.column("Stok", width=100, anchor=CENTER)
tree.pack(fill=BOTH, expand=True)

# Bind Auto-Fill ke TreeView
tree.bind("<<TreeviewSelect>>", auto_fill_form)

# Pencarian
frame_cari = Frame(root, bg="#DCEEFF", pady=10)
frame_cari.pack()
Label(frame_cari, text="Cari Produk:", bg="#DCEEFF", font=("Arial", 10)).pack(side=LEFT, padx=5)
entry_cari = Entry(frame_cari, width=30)
entry_cari.pack(side=LEFT, padx=5)
Button(frame_cari, text="Cari", command=cari_produk, bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)

# Menampilkan Data Saat Aplikasi Dibuka
tampilkan_data()

root.mainloop()
