# database.py
# Modul koneksi dan operasi database

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✓ Koneksi database berhasil")
                return True
        except Error as e:
            print(f"✗ Error koneksi database: {e}")
            return False
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("✓ Koneksi database ditutup")
    
    def execute_query(self, query, params=None):
        """Eksekusi query INSERT, UPDATE, DELETE"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error execute query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query, params=None):
        """Mengambil semua data (SELECT)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetch data: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Mengambil satu data (SELECT)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Error fetch data: {e}")
            return None

# Fungsi helper untuk operasi umum
class UserDB:
    """Class untuk operasi tabel users"""
    
    @staticmethod
    def login(db, username, password):
        """Cek login user"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND is_active = 1"
        return db.fetch_one(query, (username, password))
    
    @staticmethod
    def get_all_users(db):
        """Ambil semua user"""
        query = "SELECT * FROM users ORDER BY tgl_daftar DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def add_user(db, data):
        """Tambah user baru"""
        query = """INSERT INTO users (username, password, nama_lengkap, email, no_telp, role, is_active) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (data['username'], data['password'], data['nama_lengkap'], 
                 data['email'], data['no_telp'], data['role'], data['is_active'])
        return db.execute_query(query, params)
    
    @staticmethod
    def update_user(db, id_user, data):
        """Update user"""
        query = """UPDATE users SET username=%s, password=%s, nama_lengkap=%s, 
                   email=%s, no_telp=%s, role=%s, is_active=%s WHERE id_user=%s"""
        params = (data['username'], data['password'], data['nama_lengkap'], 
                 data['email'], data['no_telp'], data['role'], data['is_active'], id_user)
        return db.execute_query(query, params)
    
    @staticmethod
    def delete_user(db, id_user):
        """Hapus user"""
        query = "DELETE FROM users WHERE id_user = %s"
        return db.execute_query(query, (id_user,))

class ProdukDB:
    """Class untuk operasi tabel produk"""
    
    @staticmethod
    def get_all_produk(db):
        """Ambil semua produk"""
        query = "SELECT * FROM produk ORDER BY tgl_dibuat DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def add_produk(db, data):
        """Tambah produk baru"""
        query = """INSERT INTO produk (nama_game, jenis_item, jumlah_item, harga, 
                   stok, deskripsi, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (data['nama_game'], data['jenis_item'], data['jumlah_item'], 
                 data['harga'], data['stok'], data['deskripsi'], data['is_active'])
        return db.execute_query(query, params)
    
    @staticmethod
    def update_produk(db, id_produk, data):
        """Update produk"""
        query = """UPDATE produk SET nama_game=%s, jenis_item=%s, jumlah_item=%s, 
                   harga=%s, stok=%s, deskripsi=%s, is_active=%s WHERE id_produk=%s"""
        params = (data['nama_game'], data['jenis_item'], data['jumlah_item'], 
                 data['harga'], data['stok'], data['deskripsi'], data['is_active'], id_produk)
        return db.execute_query(query, params)
    
    @staticmethod
    def delete_produk(db, id_produk):
        """Hapus produk"""
        query = "DELETE FROM produk WHERE id_produk = %s"
        return db.execute_query(query, (id_produk,))

class TransaksiDB:
    """Class untuk operasi tabel transaksi"""
    
    @staticmethod
    def get_all_transaksi(db):
        """Ambil semua transaksi dengan join"""
        query = """SELECT t.*, u.username, u.nama_lengkap, p.nama_game, p.jenis_item 
                   FROM transaksi t 
                   JOIN users u ON t.id_user = u.id_user 
                   JOIN produk p ON t.id_produk = p.id_produk 
                   ORDER BY t.tgl_transaksi DESC"""
        return db.fetch_all(query)
    
    @staticmethod
    def add_transaksi(db, data):
        """Tambah transaksi baru"""
        query = """INSERT INTO transaksi (id_user, id_produk, id_game_user, jumlah, 
                   total_harga, diskon, total_bayar, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (data['id_user'], data['id_produk'], data['id_game_user'], 
                 data['jumlah'], data['total_harga'], data['diskon'], 
                 data['total_bayar'], data['status'])
        return db.execute_query(query, params)
    
    @staticmethod
    def get_dashboard_stats(db):
        """Ambil statistik untuk dashboard"""
        stats = {}
        
        # Total Pendapatan
        query = "SELECT SUM(total_bayar) as total FROM transaksi WHERE status='berhasil'"
        result = db.fetch_one(query)
        stats['total_pendapatan'] = result['total'] if result['total'] else 0
        
        # Total Transaksi
        query = "SELECT COUNT(*) as total FROM transaksi WHERE status='berhasil'"
        result = db.fetch_one(query)
        stats['total_transaksi'] = result['total'] if result['total'] else 0
        
        # Total User
        query = "SELECT COUNT(*) as total FROM users WHERE is_active=1"
        result = db.fetch_one(query)
        stats['total_user'] = result['total'] if result['total'] else 0
        
        # Produk Aktif
        query = "SELECT COUNT(*) as total FROM produk WHERE is_active=1"
        result = db.fetch_one(query)
        stats['produk_aktif'] = result['total'] if result['total'] else 0
        
        return stats