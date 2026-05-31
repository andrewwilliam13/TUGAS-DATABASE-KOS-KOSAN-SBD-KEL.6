import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QTableWidgetItem, QMessageBox
)
from PyQt5 import uic
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_window.ui", self)

        self.db = Database()
        self.btn_tambah_penyewa.clicked.connect(self.tambah_penyewa)
        self.btn_hapus_penyewa.clicked.connect(self.hapus_penyewa)
        self.btn_refresh.clicked.connect(self.refresh_semua)

        self.refresh_semua()

    def refresh_semua(self):
        self.load_penyewa()
        self.load_kamar()
        self.load_kontrak()
        self.load_pembayaran()
        self.load_komplain()

    
    def load_tabel(self, widget, headers, data):
        """Helper umum untuk isi QTableWidget"""
        widget.setColumnCount(len(headers))
        widget.setHorizontalHeaderLabels(headers)
        widget.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row.values()):
                widget.setItem(
                    row_idx, col_idx,
                    QTableWidgetItem(str(value) if value else "")
                )
        widget.resizeColumnsToContents()

    def load_penyewa(self):
        self.load_tabel(
            self.tbl_penyewa,
            ['ID', 'NIK', 'Nama', 'No Telepon'],
            self.db.get_all_penyewa()
        )

    def load_kamar(self):
        self.load_tabel(
            self.tbl_kamar,
            ['ID Kamar', 'Status'],
            self.db.get_all_kamar()
        )

    def load_kontrak(self):
        self.load_tabel(
            self.tbl_kontrak,
            ['ID Kontrak', 'Nama Penyewa', 'ID Kamar', 'Durasi', 'Status'],
            self.db.get_all_kontrak()
        )

    def load_pembayaran(self):
        self.load_tabel(
            self.tbl_pembayaran,
            ['ID Bayar', 'Nama Penyewa', 'ID Kamar', 'Nominal'],
            self.db.get_all_pembayaran()
        )

    def load_komplain(self):
        self.load_tabel(
            self.tbl_komplain,
            ['ID Komplain', 'Nama Penyewa', 'ID Kamar', 'Pesan'],
            self.db.get_all_komplain()
        )

    def tambah_penyewa(self):
        id_p  = self.input_id.text().strip()
        nik   = self.input_nik.text().strip()
        nama  = self.input_nama.text().strip()
        telp  = self.input_telepon.text().strip()

        if not id_p or not nik or not nama:
            QMessageBox.warning(self, "Input Kosong", "ID, NIK, dan Nama wajib diisi!")
            return

        try:
            self.db.tambah_penyewa(id_p, nik, nama, telp)
            QMessageBox.information(self, "Berhasil", "Penyewa berhasil ditambahkan!")
            self.input_id.clear()
            self.input_nik.clear()
            self.input_nama.clear()
            self.input_telepon.clear()
            self.load_penyewa()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def hapus_penyewa(self):
        selected = self.tbl_penyewa.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Pilih Data", "Pilih baris yang ingin dihapus!")
            return

        id_penyewa = self.tbl_penyewa.item(selected, 0).text()
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi", f"Hapus penyewa ID {id_penyewa}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            self.db.hapus_penyewa(id_penyewa)
            self.load_penyewa()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())