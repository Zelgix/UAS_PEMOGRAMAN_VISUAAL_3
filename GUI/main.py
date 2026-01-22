import sys
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from database import Database, UserDB
from ui_controller import UIController

# Import semua UI
from Login import Ui_dialogLogin
from Dashboard import Ui_Form as Ui_Dashboard
from ManajemenProduk import Ui_Form as Ui_ManajemenProduk
from DataUser import Ui_Form as Ui_DataUser
from TransaksiTopUp import Ui_Form as Ui_TransaksiTopUp
from Laporan import Ui_Form as Ui_Laporan
from NotifikasiDiskon import Ui_Form as Ui_NotifikasiDiskon

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dialogLogin()
        self.ui.setupUi(self)
        self.db = Database()
        self.db.connect()
        
        self.ui.btnLogin.clicked.connect(self.login)
        self.setWindowTitle("SITGO - Login")
        
    def login(self):
        username = self.ui.txtUsername.text()
        password = self.ui.txtUsername_2.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Peringatan", "Username dan Password harus diisi")
            return
        
        user = UserDB.login(self.db, username, password)
        
        if user:
            self.user_data = user
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Username atau Password salah")

class MainWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.db = Database()
        self.db.connect()
        
        self.stacked_widget = QStackedWidget()
        self.controller = UIController(self.db, self.user_data)
        
        self.init_pages()
        self.setup_navigation()
        
        self.resize(1433, 895)
        self.setWindowTitle("SITGO - Sistem Top-Up Game Online")
        
    def init_pages(self):
        # Dashboard
        self.dashboard = QWidget()
        self.ui_dashboard = Ui_Dashboard()
        self.ui_dashboard.setupUi(self.dashboard)
        self.stacked_widget.addWidget(self.dashboard)
        
        # Manajemen Produk
        self.produk = QWidget()
        self.ui_produk = Ui_ManajemenProduk()
        self.ui_produk.setupUi(self.produk)
        self.stacked_widget.addWidget(self.produk)
        
        # Transaksi
        self.transaksi = QWidget()
        self.ui_transaksi = Ui_TransaksiTopUp()
        self.ui_transaksi.setupUi(self.transaksi)
        self.stacked_widget.addWidget(self.transaksi)
        
        # Data User
        self.user = QWidget()
        self.ui_user = Ui_DataUser()
        self.ui_user.setupUi(self.user)
        self.stacked_widget.addWidget(self.user)
        
        # Laporan
        self.laporan = QWidget()
        self.ui_laporan = Ui_Laporan()
        self.ui_laporan.setupUi(self.laporan)
        self.stacked_widget.addWidget(self.laporan)
        
        # Notifikasi
        self.notifikasi = QWidget()
        self.ui_notifikasi = Ui_NotifikasiDiskon()
        self.ui_notifikasi.setupUi(self.notifikasi)
        self.stacked_widget.addWidget(self.notifikasi)
        
        # Load data awal
        self.controller.load_dashboard(self.ui_dashboard)
        self.controller.load_produk(self.ui_produk)
        self.controller.load_transaksi(self.ui_transaksi)
        self.controller.load_users(self.ui_user)
        
    def setup_navigation(self):
        # Dashboard navigation
        self.ui_dashboard.btnDashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_dashboard.btnProduk.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_dashboard.btnTransaksi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_dashboard.btnUser.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_dashboard.btnLaporan.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_dashboard.btnNotifikasi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_dashboard.btnLogout.clicked.connect(self.logout)
        
        # Produk navigation
        self.ui_produk.btnDashboard_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_produk.btnProduk_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_produk.btnTransaksi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_produk.btnUser_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_produk.btnLaporan_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_produk.btnNotifikasi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_produk.btnLogout_2.clicked.connect(self.logout)
        
        # Transaksi navigation
        self.ui_transaksi.btnDashboard_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_transaksi.btnProduk_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_transaksi.btnTransaksi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_transaksi.btnUser_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_transaksi.btnLaporan_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_transaksi.btnNotifikasi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_transaksi.btnLogout_2.clicked.connect(self.logout)
        
        # User navigation
        self.ui_user.btnDashboard_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_user.btnProduk_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_user.btnTransaksi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_user.btnUser_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_user.btnLaporan_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_user.btnNotifikasi_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_user.btnLogout_2.clicked.connect(self.logout)
        
        # Laporan navigation
        self.ui_laporan.btnDashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_laporan.btnProduk.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_laporan.btnTransaksi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_laporan.btnUser.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_laporan.btnLaporan.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_laporan.btnNotifikasi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_laporan.btnLogout.clicked.connect(self.logout)
        
        # Notifikasi navigation
        self.ui_notifikasi.btnDashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ui_notifikasi.btnProduk.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui_notifikasi.btnTransaksi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.ui_notifikasi.btnUser.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.ui_notifikasi.btnLaporan.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ui_notifikasi.btnNotifikasi.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ui_notifikasi.btnLogout.clicked.connect(self.logout)
        
        # Setup button handlers
        self.controller.setup_produk_handlers(self.ui_produk)
        self.controller.setup_user_handlers(self.ui_user)
        self.controller.setup_transaksi_handlers(self.ui_transaksi)
        self.controller.setup_laporan_handlers(self.ui_laporan)
        self.controller.setup_notifikasi_handlers(self.ui_notifikasi)
        
    def logout(self):
        reply = QMessageBox.question(self, 'Konfirmasi', 
                                     'Yakin ingin logout?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def show(self):
        self.stacked_widget.show()

def main():
    app = QApplication(sys.argv)
    
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        main_window = MainWindow(login.user_data)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()