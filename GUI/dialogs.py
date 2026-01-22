from PyQt5.QtWidgets import QDialog, QMessageBox
from database import ProdukDB, UserDB
from TambahProduk import Ui_dialogTambahProduk
from EditProduk import Ui_Dialog as Ui_EditProduk
from HapusProduk import Ui_dialogDelete
from TambahUserBaru import Ui_Dialog as Ui_TambahUser
from EditUser import Ui_Dialog as Ui_EditUser
from HapusUser import Ui_Dialog as Ui_HapusUser
from EditEvent import Ui_Dialog as Ui_EditEvent
from HapusEvent import Ui_Dialog as Ui_HapusEvent

class TambahProdukDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_dialogTambahProduk()
        self.ui.setupUi(self)
        self.ui.btnSimpan.clicked.connect(self.simpan)
        self.ui.btnBatal.clicked.connect(self.reject)
        
    def simpan(self):
        if self.ui.cmbJenisItem.currentIndex() == 0:
            QMessageBox.warning(self, "Peringatan", "Pilih nama game")
            return
        
        data = {
            'nama_game': self.ui.cmbJenisItem.currentText(),
            'jenis_item': self.ui.cmbJenisItem_2.currentText(),
            'jumlah_item': self.ui.spinJumlah.value(),
            'harga': int(self.ui.txtHarga.text().strip()),
            'stok': self.ui.spinStok.value(),
            'deskripsi': self.ui.txtDeskripsi.toPlainText(),
            'is_active': 1 if self.ui.cmbStatus.currentText() == "Aktif" else 0
        }
        
        if ProdukDB.add_produk(self.db, data):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Gagal menambah produk")

class EditProdukDialog(QDialog):
    def __init__(self, db, id_produk):
        super().__init__()
        self.db = db
        self.id_produk = id_produk
        self.ui = Ui_EditProduk()
        self.ui.setupUi(self)
        
        produk = db.fetch_one("SELECT * FROM produk WHERE id_produk = %s", (id_produk,))
        if produk:
            self.ui.txtID.setText(str(produk['id_produk']))
            idx = self.ui.cmbJenisItem.findText(produk['nama_game'])
            if idx >= 0:
                self.ui.cmbJenisItem.setCurrentIndex(idx)
            idx = self.ui.cmbJenisItem_2.findText(produk['jenis_item'])
            if idx >= 0:
                self.ui.cmbJenisItem_2.setCurrentIndex(idx)
            self.ui.spinJumlah.setValue(produk['jumlah_item'])
            self.ui.txtHarga.setText(str(produk['harga']))
            self.ui.spinStok.setValue(produk['stok'])
            self.ui.txtDeskripsi.setPlainText(produk['deskripsi'] or "")
            self.ui.mbStatus.setCurrentIndex(0 if produk['is_active'] else 1)
        
        self.ui.btnUpdate.clicked.connect(self.update)
        self.ui.btnBatal.clicked.connect(self.reject)
        self.ui.btnClose.clicked.connect(self.reject)
        
    def update(self):
        data = {
            'nama_game': self.ui.cmbJenisItem.currentText(),
            'jenis_item': self.ui.cmbJenisItem_2.currentText(),
            'jumlah_item': self.ui.spinJumlah.value(),
            'harga': int(self.ui.txtHarga.text().strip()),
            'stok': self.ui.spinStok.value(),
            'deskripsi': self.ui.txtDeskripsi.toPlainText(),
            'is_active': 1 if self.ui.mbStatus.currentText() == "Aktif" else 0
        }
        
        if ProdukDB.update_produk(self.db, self.id_produk, data):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Gagal update produk")

class HapusProdukDialog(QDialog):
    def __init__(self, id_produk, nama):
        super().__init__()
        self.id_produk = id_produk
        self.ui = Ui_dialogDelete()
        self.ui.setupUi(self)
        self.ui.lblInfoProduk.setText(f"ID: {id_produk} - {nama}")
        self.ui.btnHapus.clicked.connect(self.accept)
        self.ui.btnBatal.clicked.connect(self.reject)

class TambahUserDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_TambahUser()
        self.ui.setupUi(self)
        self.ui.btnSimpan.clicked.connect(self.simpan)
        self.ui.btnBatal.clicked.connect(self.reject)
        self.ui.btnClose.clicked.connect(self.reject)
        
    def simpan(self):
        if not self.ui.txtUssername.text():
            QMessageBox.warning(self, "Peringatan", "Username harus diisi")
            return
        
        data = {
            'username': self.ui.txtUssername.text(),
            'password': self.ui.txtPassword.text(),
            'nama_lengkap': self.ui.txtNamaLengkap.text(),
            'email': self.ui.txtEmail.text(),
            'no_telp': self.ui.txtNoTelp.text(),
            'role': self.ui.cmbRole.currentText(),
            'is_active': 1 if self.ui.cmbStatus.currentText() == "Aktif" else 0
        }
        
        if UserDB.add_user(self.db, data):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Gagal menambah user")

class EditUserDialog(QDialog):
    def __init__(self, db, id_user):
        super().__init__()
        self.db = db
        self.id_user = id_user
        self.ui = Ui_EditUser()
        self.ui.setupUi(self)
        
        user = db.fetch_one("SELECT * FROM users WHERE id_user = %s", (id_user,))
        if user:
            self.ui.txtIdUser.setText(str(user['id_user']))
            self.ui.txtUssername.setText(user['username'])
            self.ui.txtPassword.setText(user['password'])
            self.ui.txtNamaLengkap.setText(user['nama_lengkap'])
            self.ui.txtEmail.setText(user['email'])
            self.ui.txtNoTelp.setText(user['no_telp'])
            idx = self.ui.cmbRole.findText(user['role'])
            if idx >= 0:
                self.ui.cmbRole.setCurrentIndex(idx)
            self.ui.cmbStatus.setCurrentIndex(0 if user['is_active'] else 1)
        
        self.ui.btnSimpan.clicked.connect(self.update)
        self.ui.btnBatal.clicked.connect(self.reject)
        self.ui.btnClose.clicked.connect(self.reject)
        
    def update(self):
        data = {
            'username': self.ui.txtUssername.text(),
            'password': self.ui.txtPassword.text(),
            'nama_lengkap': self.ui.txtNamaLengkap.text(),
            'email': self.ui.txtEmail.text(),
            'no_telp': self.ui.txtNoTelp.text(),
            'role': self.ui.cmbRole.currentText(),
            'is_active': 1 if self.ui.cmbStatus.currentText() == "Aktif" else 0
        }
        
        if UserDB.update_user(self.db, self.id_user, data):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Gagal update user")

class HapusUserDialog(QDialog):
    def __init__(self, id_user, nama):
        super().__init__()
        self.id_user = id_user
        self.ui = Ui_HapusUser()
        self.ui.setupUi(self)
        self.ui.lblNamaUser.setText(f"ID: {id_user} - {nama}")
        self.ui.btnHapus.clicked.connect(self.accept)
        self.ui.btnBatal.clicked.connect(self.reject)

class TambahEventDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_EditEvent()
        self.ui.setupUi(self)
        self.ui.btnUpdate.setText("Simpan Event")
        self.ui.btnUpdate.clicked.connect(self.accept)
        self.ui.btnBatal.clicked.connect(self.reject)
        self.ui.btnClose.clicked.connect(self.reject)

class EditEventDialog(QDialog):
    def __init__(self, db, id_event):
        super().__init__()
        self.db = db
        self.id_event = id_event
        self.ui = Ui_EditEvent()
        self.ui.setupUi(self)
        self.ui.btnUpdate.clicked.connect(self.accept)
        self.ui.btnBatal.clicked.connect(self.reject)
        self.ui.btnClose.clicked.connect(self.reject)

class HapusEventDialog(QDialog):
    def __init__(self, id_event, nama):
        super().__init__()
        self.id_event = id_event
        self.ui = Ui_HapusEvent()
        self.ui.setupUi(self)
        self.ui.lblNamaEvent.setText(f"ID: {id_event} - {nama}")
        self.ui.btnHapus.clicked.connect(self.accept)
        self.ui.btnBatal.clicked.connect(self.reject)