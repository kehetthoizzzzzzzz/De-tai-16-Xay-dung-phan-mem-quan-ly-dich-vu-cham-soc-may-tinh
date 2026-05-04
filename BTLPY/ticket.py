from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
import sqlite3


class Ui_MainWindow(QtCore.QObject):
    ticket_created = QtCore.pyqtSignal()

    def setupUi(self, MainWindow):
        super().__init__()

        MainWindow.resize(700, 550)
        MainWindow.setWindowTitle("Tạo ticket sửa chữa")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("""
            background-color: #ecf0f3;
        """)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(500)
        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
            }
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setYOffset(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.card.setGraphicsEffect(shadow)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 20, 30, 20)
        card_layout.setSpacing(15)

        # ===== TITLE =====
        title = QtWidgets.QLabel("🎫 Tạo ticket sửa chữa")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)
        card_layout.addWidget(title)

        # ===== INPUT =====
        def input_field(placeholder):
            line = QtWidgets.QLineEdit()
            line.setPlaceholderText(placeholder)
            line.setMinimumHeight(35)
            line.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 2px solid #bdc3c7;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border-bottom: 2px solid #3498db;
                }
            """)
            return line

        def combo_box(placeholder):
            cb = QtWidgets.QComboBox()
            cb.setMinimumHeight(35)
            cb.setStyleSheet("""
                QComboBox {
                    border: none;
                    border-bottom: 2px solid #bdc3c7;
                    padding: 5px;
                }
                QComboBox:focus {
                    border-bottom: 2px solid #3498db;
                }
            """)
            cb.setEditable(True)
            cb.lineEdit().setPlaceholderText(placeholder)
            cb.lineEdit().setReadOnly(True)
            return cb

        # ===== COMPONENTS =====
        self.cb_khach = combo_box("Chọn khách hàng")
        self.cb_nv = combo_box("Nhân viên xử lý")

        self.type = input_field("Loại máy")
        self.problem = input_field("Vấn đề")
        self.device = input_field("Tên máy")

        self.desc = QtWidgets.QTextEdit()
        self.desc.setPlaceholderText("Mô tả tình trạng lỗi...")
        self.desc.setFixedHeight(70)

        # ===== GIÁ TIỀN =====
        self.gia = input_field("Nhập giá (VND)")
        self.gia.setValidator(QIntValidator(0, 1000000000))

        for w in [self.cb_khach, self.cb_nv, self.type, self.problem, self.device, self.desc, self.gia]:
            card_layout.addWidget(w)

        # ===== BUTTON =====
        btn_layout = QtWidgets.QHBoxLayout()

        self.btn_create = QtWidgets.QPushButton("Tạo ticket")
        self.btn_cancel = QtWidgets.QPushButton("Hủy")

        self.btn_create.setStyleSheet("background:#3498db;color:white;padding:10px;border-radius:8px;")
        self.btn_cancel.setStyleSheet("background:#e74c3c;color:white;padding:10px;border-radius:8px;")

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)

        card_layout.addLayout(btn_layout)
        main_layout.addWidget(self.card)

        # ===== INIT DB =====
        self.init_db()
        self.load_khach()
        self.load_nv()

        # ===== EVENT =====
        self.btn_create.clicked.connect(self.create_ticket)
        self.btn_cancel.clicked.connect(MainWindow.close)

    # ========================
    # DATABASE
    # ========================
    def init_db(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

    def load_khach(self):
        self.cb_khach.clear()
        for row in self.cursor.execute("SELECT id_khach, ten FROM customers"):
            self.cb_khach.addItem(row[1], row[0])

    def load_nv(self):
        self.cb_nv.clear()
        for row in self.cursor.execute("SELECT id_nv, ten FROM staff"):
            self.cb_nv.addItem(row[1], row[0])

    # ========================
    # CREATE TICKET
    # ========================
    def create_ticket(self):
        id_khach = self.cb_khach.currentData()
        id_nv = self.cb_nv.currentData()

        loai = self.type.text()
        loi = self.problem.text()
        tenmay = self.device.text()
        mota = self.desc.toPlainText()
        gia = self.gia.text()

        if not id_khach or not id_nv:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Chọn khách và nhân viên!")
            return

        if not gia:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Nhập giá!")
            return

        gia = int(gia)

        query = """
        INSERT INTO ticket (id_khach, id_nv, loai_may, loi, ten_may, mo_ta, gia_tien)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(query, (id_khach, id_nv, loai, loi, tenmay, mota, gia))
        self.conn.commit()

        QtWidgets.QMessageBox.information(None, "Thành công", "Đã tạo ticket!")

        # 🔥 realtime update
        self.ticket_created.emit()

        # reset form
        self.type.clear()
        self.problem.clear()
        self.device.clear()
        self.desc.clear()
        self.gia.clear()


# ========================
# RUN APP
# ========================
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec())