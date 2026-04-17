from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QMessageBox
import sys
import main   # import file main.py

class Ui_Login(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("LoginWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # ===== LAYOUT CHÍNH =====
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("card")
        self.card.setFixedSize(400, 380)
        main_layout.addWidget(self.card)

        # ===== LAYOUT CARD =====
        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(40, 20, 40, 20)

        # ===== TITLE =====
        self.dang_nhap = QtWidgets.QLabel("Đăng nhập")
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.dang_nhap.setFont(font)
        self.dang_nhap.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== INPUT =====
        self.ten_dang_nhap = QtWidgets.QLineEdit()
        self.ten_dang_nhap.setPlaceholderText("👤 Tên đăng nhập")

        self.mat_khau = QtWidgets.QLineEdit()
        self.mat_khau.setPlaceholderText("🔒 Mật khẩu")
        self.mat_khau.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.sdt_email = QtWidgets.QLineEdit()
        self.sdt_email.setPlaceholderText("📧 SĐT / Email")

        # ===== BUTTON =====
        self.btn_login = QtWidgets.QPushButton("Đăng nhập")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setFixedHeight(40)

        self.btn_register = QtWidgets.QPushButton("Đăng ký")
        self.btn_register.setObjectName("btn_register")

        self.btn_forgot = QtWidgets.QPushButton("Quên mật khẩu")
        self.btn_forgot.setObjectName("btn_forgot")

        # ===== ADD WIDGET =====
        card_layout.addWidget(self.dang_nhap)
        card_layout.addWidget(self.ten_dang_nhap)
        card_layout.addWidget(self.mat_khau)
        card_layout.addWidget(self.sdt_email)
        card_layout.addWidget(self.btn_login)

        # ===== BUTTON ROW =====
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_forgot)
        card_layout.addLayout(btn_layout)

        # ===== STYLE =====
        MainWindow.setStyleSheet("""
        QMainWindow { background-color: #f5f7fb; }
        QFrame#card { background: white; border-radius: 15px; }
        QLabel { color: #2f80ed; }
        QLineEdit {
            border: 1px solid #ddd; border-radius: 10px;
            padding: 10px; background: white;
        }
        QLineEdit:focus { border: 2px solid #2f80ed; }
        QPushButton { border-radius: 10px; font-weight: bold; padding: 8px; }
        QPushButton#btn_login {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #56CCF2, stop:1 #2F80ED);
            color: white;
        }
        QPushButton#btn_login:hover { background: #2F80ED; }
        QPushButton#btn_register { background: #27AE60; color: white; }
        QPushButton#btn_register:hover { background: #219150; }
        QPushButton#btn_forgot {
            background: transparent; color: #2F80ED; border: none;
        }
        QPushButton#btn_forgot:hover { text-decoration: underline; }
        """)

        # ===== SHADOW =====
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 5)
        self.card.setGraphicsEffect(shadow)

        # Kết nối nút login
        self.btn_login.clicked.connect(self.handle_login)
        self.MainWindow = MainWindow

    def handle_login(self):
        username = self.ten_dang_nhap.text()
        password = self.mat_khau.text()

        if username == "admin" and password == "123":
            self.open_main_app()
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    def open_main_app(self):
        self.MainWindow.close()
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main = main.Ui_MainWindow()
        self.ui_main.setupUi(self.main_window)
        self.main_window.show()


# ===== RUN =====
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_win = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(login_win)
    login_win.show()
    sys.exit(app.exec())
