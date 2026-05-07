from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sys

users = {}

# ===== TRANG CHỦ =====
class HomeWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(900, 500)

        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("""
            background: #2f80ed;
            color: white;
            border-radius: 10px;
        """)
        side_layout = QVBoxLayout()
        side_layout.addWidget(QLabel("🏠 Dashboard"))
        side_layout.addWidget(QLabel("📦 Quản lý"))
        side_layout.addWidget(QLabel("👤 Khách hàng"))
        side_layout.addStretch()
        sidebar.setLayout(side_layout)

        # Nội dung
        content = QVBoxLayout()

        welcome = QLabel(f"Xin chào, {user} 👋")
        welcome.setStyleSheet("font-size: 20px; font-weight: bold;")

        card1 = self.create_card("12 Máy đang sửa", "#56CCF2")
        card2 = self.create_card("5.2 triệu", "#F2994A")
        card3 = self.create_card("3 linh kiện sắp hết", "#6FCF97")

        row = QHBoxLayout()
        row.addWidget(card1)
        row.addWidget(card2)
        row.addWidget(card3)

        content.addWidget(welcome)
        content.addLayout(row)

        main_layout.addWidget(sidebar)
        main_layout.addLayout(content)

        self.setLayout(main_layout)

    def create_card(self, text, color):
        card = QFrame()
        card.setStyleSheet(f"""
            background: {color};
            color: white;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text))
        card.setLayout(layout)
        return card


# ===== APP LOGIN =====
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống")
        self.resize(800, 500)

        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("""
            background: #2f80ed;
            border-radius: 10px;
        """)
        main_layout.addWidget(sidebar)

        # Nội dung chính
        content = QVBoxLayout()

        self.tabs = QTabWidget()

        # ===== ĐĂNG KÝ =====
        tab_reg = QWidget()
        reg_layout = QVBoxLayout()

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Tên đăng nhập")

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Mật khẩu")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)

        btn_reg = QPushButton("Đăng ký")
        btn_reg.clicked.connect(self.register)

        reg_layout.addWidget(self.create_card("Đăng ký", [
            self.reg_user,
            self.reg_pass,
            btn_reg
        ]))

        tab_reg.setLayout(reg_layout)

        # ===== ĐĂNG NHẬP =====
        tab_login = QWidget()
        login_layout = QVBoxLayout()

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Tên đăng nhập")

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Mật khẩu")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Đăng nhập")
        btn_login.clicked.connect(self.login)

        login_layout.addWidget(self.create_card("Đăng nhập", [
            self.login_user,
            self.login_pass,
            btn_login
        ]))

        tab_login.setLayout(login_layout)

        self.tabs.addTab(tab_reg, "Đăng ký")
        self.tabs.addTab(tab_login, "Đăng nhập")

        content.addWidget(self.tabs)

        main_layout.addLayout(content)
        self.setLayout(main_layout)

        # STYLE
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fb;
                font-family: Segoe UI;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: white;
            }

            QPushButton {
                background-color: #2f80ed;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1c60c7;
            }

            QTabBar::tab {
                background: #ddd;
                padding: 10px;
                border-radius: 8px;
                margin: 3px;
            }

            QTabBar::tab:selected {
                background: #2f80ed;
                color: white;
            }
        """)

    def create_card(self, title, widgets):
        card = QFrame()
        card.setStyleSheet("""
            background: white;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        for w in widgets:
            layout.addWidget(w)
        card.setLayout(layout)
        return card

    def register(self):
        user = self.reg_user.text()
        password = self.reg_pass.text()

        if not user or not password:
            QMessageBox.warning(self, "Lỗi", "Nhập đầy đủ!")
            return

        if user in users:
            QMessageBox.warning(self, "Lỗi", "Tài khoản tồn tại!")
            return

        users[user] = password
        QMessageBox.information(self, "OK", "Đăng ký thành công!")

    def login(self):
        user = self.login_user.text()
        password = self.login_pass.text()

        if user in users and users[user] == password:
            self.home = HomeWindow(user)
            self.home.show()
            self.close()
        else:
            QMessageBox.warning(self, "Sai", "Sai tài khoản!")

# RUN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())