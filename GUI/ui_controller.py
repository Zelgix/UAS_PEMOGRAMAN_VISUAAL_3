from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from datetime import datetime
from database import UserDB, ProdukDB, TransaksiDB
from dialogs import TambahProdukDialog, EditProdukDialog, HapusProdukDialog
from dialogs import TambahUserDialog, EditUserDialog, HapusUserDialog
from dialogs import TambahEventDialog, EditEventDialog, HapusEventDialog
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class UIController:
    def __init__(self, db, user_data):
        self.db = db
        self.user_data = user_data
        
    def load_dashboard(self, ui):
        stats = TransaksiDB.get_dashboard_stats(self.db)
        ui.lblTotalPendapatan.setText(f"Rp {stats['total_pendapatan']:,.0f}")
        ui.lblTotalTransaksi.setText(f"{stats['total_transaksi']}")
        ui.lblTotalUser.setText(f"{stats['total_user']}")
        ui.lblProdukAktif.setText(f"{stats['produk_aktif']}")
        
        transaksi = TransaksiDB.get_all_transaksi(self.db)
        ui.tblTransaksiTerakhir.setRowCount(0)
        
        for i, row in enumerate(transaksi[:10]):
            ui.tblTransaksiTerakhir.insertRow(i)
            ui.tblTransaksiTerakhir.setItem(i, 0, QTableWidgetItem(str(row['id_transaksi'])))
            ui.tblTransaksiTerakhir.setItem(i, 1, QTableWidgetItem(row['username']))
            ui.tblTransaksiTerakhir.setItem(i, 2, QTableWidgetItem(f"{row['nama_game']} - {row['jenis_item']}"))
            ui.tblTransaksiTerakhir.setItem(i, 3, QTableWidgetItem(f"Rp {row['total_bayar']:,.0f}"))
            ui.tblTransaksiTerakhir.setItem(i, 4, QTableWidgetItem(row['status'].capitalize()))
            ui.tblTransaksiTerakhir.setItem(i, 5, QTableWidgetItem(row['tgl_transaksi'].strftime('%Y-%m-%d %H:%M')))
    
    def load_produk(self, ui):
        produk = ProdukDB.get_all_produk(self.db)
        ui.tblProduk.setRowCount(0)
        
        for i, row in enumerate(produk):
            ui.tblProduk.insertRow(i)
            ui.tblProduk.setItem(i, 0, QTableWidgetItem(str(row['id_produk'])))
            ui.tblProduk.setItem(i, 1, QTableWidgetItem(row['nama_game']))
            ui.tblProduk.setItem(i, 2, QTableWidgetItem(row['jenis_item']))
            ui.tblProduk.setItem(i, 3, QTableWidgetItem(str(row['jumlah_item'])))
            ui.tblProduk.setItem(i, 4, QTableWidgetItem(f"Rp {row['harga']:,.0f}"))
            ui.tblProduk.setItem(i, 5, QTableWidgetItem(str(row['stok'])))
            ui.tblProduk.setItem(i, 6, QTableWidgetItem("Aktif" if row['is_active'] else "Tidak Aktif"))
    
    def load_users(self, ui):
        users = UserDB.get_all_users(self.db)
        ui.tblDataUser.setRowCount(0)
        
        total = len(users)
        aktif = len([u for u in users if u['is_active']])
        baru = len([u for u in users if (datetime.now() - u['tgl_daftar']).days <= 30])
        
        ui.lblTotalUser_3.setText(str(total))
        ui.lblUserAktif.setText(str(aktif))
        ui.lblUserBaru.setText(str(baru))
        
        for i, row in enumerate(users):
            ui.tblDataUser.insertRow(i)
            ui.tblDataUser.setItem(i, 0, QTableWidgetItem(str(row['id_user'])))
            ui.tblDataUser.setItem(i, 1, QTableWidgetItem(row['username']))
            ui.tblDataUser.setItem(i, 2, QTableWidgetItem(row['nama_lengkap']))
            ui.tblDataUser.setItem(i, 3, QTableWidgetItem(row['email']))
            ui.tblDataUser.setItem(i, 4, QTableWidgetItem(row['no_telp']))
            ui.tblDataUser.setItem(i, 5, QTableWidgetItem(row['role']))
            ui.tblDataUser.setItem(i, 6, QTableWidgetItem("Aktif" if row['is_active'] else "Tidak Aktif"))
            ui.tblDataUser.setItem(i, 7, QTableWidgetItem(row['tgl_daftar'].strftime('%Y-%m-%d')))
    
    def load_transaksi(self, ui):
        transaksi = TransaksiDB.get_all_transaksi(self.db)
        ui.tblRiwayatTransaksit.setRowCount(0)
        
        for i, row in enumerate(transaksi):
            ui.tblRiwayatTransaksit.insertRow(i)
            ui.tblRiwayatTransaksit.setItem(i, 0, QTableWidgetItem(str(row['id_transaksi'])))
            ui.tblRiwayatTransaksit.setItem(i, 1, QTableWidgetItem(row['username']))
            ui.tblRiwayatTransaksit.setItem(i, 2, QTableWidgetItem(f"{row['nama_game']} - {row['jenis_item']}"))
            ui.tblRiwayatTransaksit.setItem(i, 3, QTableWidgetItem(row['id_game_user']))
            ui.tblRiwayatTransaksit.setItem(i, 4, QTableWidgetItem(f"Rp {row['total_bayar']:,.0f}"))
            ui.tblRiwayatTransaksit.setItem(i, 5, QTableWidgetItem(row.get('metode_bayar', '-')))
            ui.tblRiwayatTransaksit.setItem(i, 6, QTableWidgetItem(row['status'].capitalize()))
            ui.tblRiwayatTransaksit.setItem(i, 7, QTableWidgetItem(row['tgl_transaksi'].strftime('%Y-%m-%d')))
        
        users = UserDB.get_all_users(self.db)
        produk = ProdukDB.get_all_produk(self.db)
        
        ui.cmbPilihUser.clear()
        ui.cmbPilihUser.addItem("-- Pilih User --")
        for user in users:
            ui.cmbPilihUser.addItem(f"{user['username']} - {user['nama_lengkap']}", user['id_user'])
        
        ui.cmbPilihProduk.clear()
        ui.cmbPilihProduk.addItem("-- Pilih Produk --")
        for p in produk:
            ui.cmbPilihProduk.addItem(f"{p['nama_game']} - {p['jenis_item']} ({p['jumlah_item']})", p['id_produk'])
    
    def setup_produk_handlers(self, ui):
        ui.btnTambahProduk.clicked.connect(lambda: self.tambah_produk(ui))
        ui.tblProduk.itemSelectionChanged.connect(lambda: self.produk_selection_changed(ui))
        ui.btnEdit.clicked.connect(lambda: self.edit_produk(ui))
        ui.btnHapus.clicked.connect(lambda: self.hapus_produk(ui))
    
    def setup_user_handlers(self, ui):
        ui.btnTambahUser.clicked.connect(lambda: self.tambah_user(ui))
        ui.tblDataUser.itemSelectionChanged.connect(lambda: self.user_selection_changed(ui))
        ui.btnEdit.clicked.connect(lambda: self.edit_user(ui))
        ui.btnHapus_2.clicked.connect(lambda: self.hapus_user(ui))
    
    def setup_transaksi_handlers(self, ui):
        ui.btnProsesTransaksi.clicked.connect(lambda: self.proses_transaksi(ui))
    
    def setup_laporan_handlers(self, ui):
        ui.btnGenerate.clicked.connect(lambda: self.generate_laporan(ui))
        ui.btnExportPDF.clicked.connect(lambda: self.export_pdf(ui))
    
    def setup_notifikasi_handlers(self, ui):
        ui.btnBuatEvent.clicked.connect(lambda: self.buat_event(ui))
        ui.btnEdit.clicked.connect(lambda: self.edit_event(ui))
        ui.btnHapus.clicked.connect(lambda: self.hapus_event(ui))
    
    def tambah_produk(self, ui):
        dialog = TambahProdukDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_produk(ui)
            QMessageBox.information(None, "Sukses", "Produk berhasil ditambahkan")
    
    def edit_produk(self, ui):
        if ui.tblProduk.currentRow() >= 0:
            id_produk = ui.tblProduk.item(ui.tblProduk.currentRow(), 0).text()
            dialog = EditProdukDialog(self.db, id_produk)
            if dialog.exec_() == QDialog.Accepted:
                self.load_produk(ui)
                QMessageBox.information(None, "Sukses", "Produk berhasil diupdate")
    
    def hapus_produk(self, ui):
        if ui.tblProduk.currentRow() >= 0:
            id_produk = ui.tblProduk.item(ui.tblProduk.currentRow(), 0).text()
            nama = ui.tblProduk.item(ui.tblProduk.currentRow(), 1).text()
            dialog = HapusProdukDialog(id_produk, nama)
            if dialog.exec_() == QDialog.Accepted:
                if ProdukDB.delete_produk(self.db, id_produk):
                    self.load_produk(ui)
                    QMessageBox.information(None, "Sukses", "Produk berhasil dihapus")
    
    def tambah_user(self, ui):
        dialog = TambahUserDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users(ui)
            QMessageBox.information(None, "Sukses", "User berhasil ditambahkan")
    
    def edit_user(self, ui):
        if ui.tblDataUser.currentRow() >= 0:
            id_user = ui.tblDataUser.item(ui.tblDataUser.currentRow(), 0).text()
            dialog = EditUserDialog(self.db, id_user)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users(ui)
                QMessageBox.information(None, "Sukses", "User berhasil diupdate")
    
    def hapus_user(self, ui):
        if ui.tblDataUser.currentRow() >= 0:
            id_user = ui.tblDataUser.item(ui.tblDataUser.currentRow(), 0).text()
            nama = ui.tblDataUser.item(ui.tblDataUser.currentRow(), 2).text()
            dialog = HapusUserDialog(id_user, nama)
            if dialog.exec_() == QDialog.Accepted:
                if UserDB.delete_user(self.db, id_user):
                    self.load_users(ui)
                    QMessageBox.information(None, "Sukses", "User berhasil dihapus")
    
    def proses_transaksi(self, ui):
        if ui.cmbPilihUser.currentIndex() == 0:
            QMessageBox.warning(None, "Peringatan", "Pilih user terlebih dahulu")
            return
        if ui.cmbPilihProduk.currentIndex() == 0:
            QMessageBox.warning(None, "Peringatan", "Pilih produk terlebih dahulu")
            return
        if not ui.txtIDGameUser.text():
            QMessageBox.warning(None, "Peringatan", "Masukkan ID Game User")
            return
        
        id_user = ui.cmbPilihUser.currentData()
        id_produk = ui.cmbPilihProduk.currentData()
        id_game = ui.txtIDGameUser.text()
        jumlah = ui.spinJumlah.value()
        
        produk = self.db.fetch_one("SELECT * FROM produk WHERE id_produk = %s", (id_produk,))
        total = produk['harga'] * jumlah
        
        data = {
            'id_user': id_user,
            'id_produk': id_produk,
            'id_game_user': id_game,
            'jumlah': jumlah,
            'total_harga': total,
            'diskon': 0,
            'total_bayar': total,
            'status': 'berhasil'
        }
        
        if TransaksiDB.add_transaksi(self.db, data):
            self.load_transaksi(ui)
            QMessageBox.information(None, "Sukses", "Transaksi berhasil diproses")
            ui.txtIDGameUser.clear()
            ui.txtKodeDiskon.clear()
    
    def generate_laporan(self, ui):
        transaksi = TransaksiDB.get_all_transaksi(self.db)
        ui.tblDetailTransaksi.setRowCount(0)
        
        total_pendapatan = sum(t['total_bayar'] for t in transaksi if t['status'] == 'berhasil')
        total_transaksi = len([t for t in transaksi if t['status'] == 'berhasil'])
        
        ui.lblTotalPendapatan.setText(f"Rp {total_pendapatan:,.0f}")
        ui.lblTotalTransaksi.setText(str(total_transaksi))
        
        if total_transaksi > 0:
            rata = total_pendapatan / total_transaksi
            ui.lblRataHari.setText(f"Rp {rata:,.0f}")
        
        for i, row in enumerate(transaksi[:5]):
            ui.tblDetailTransaksi.insertRow(i)
            ui.tblDetailTransaksi.setItem(i, 0, QTableWidgetItem(row['tgl_transaksi'].strftime('%Y-%m-%d')))
            ui.tblDetailTransaksi.setItem(i, 1, QTableWidgetItem("1"))
            ui.tblDetailTransaksi.setItem(i, 2, QTableWidgetItem(f"Rp {row['total_bayar']:,.0f}"))
            ui.tblDetailTransaksi.setItem(i, 3, QTableWidgetItem(row['nama_game']))
            ui.tblDetailTransaksi.setItem(i, 4, QTableWidgetItem(row['status'].capitalize()))
        
        QMessageBox.information(None, "Sukses", "Laporan berhasil digenerate")
    
    def export_pdf(self, ui):
        filename, _ = QFileDialog.getSaveFileName(None, "Export PDF", "", "PDF Files (*.pdf)")
        if filename:
            c = canvas.Canvas(filename, pagesize=A4)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, 10.5*inch, "Laporan Transaksi SITGO")
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, 10*inch, f"Tanggal: {datetime.now().strftime('%Y-%m-%d')}")
            c.save()
            QMessageBox.information(None, "Sukses", f"PDF berhasil diexport ke {filename}")
    
    def buat_event(self, ui):
        dialog = TambahEventDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(None, "Sukses", "Event berhasil dibuat")
    
    def edit_event(self, ui):
        QMessageBox.information(None, "Info", "Fitur edit event")
    
    def hapus_event(self, ui):
        QMessageBox.information(None, "Info", "Fitur hapus event")
    
    def produk_selection_changed(self, ui):
        pass
    
    def user_selection_changed(self, ui):
        pass