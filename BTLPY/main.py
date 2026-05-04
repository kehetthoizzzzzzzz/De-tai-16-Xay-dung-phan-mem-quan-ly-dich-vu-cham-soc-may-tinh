import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3

import ticket
import cskh
import kholinhkien
import Donxuly
import Nhansu
import baocao


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1100, 650)
        MainWindow.setFont(QtGui.QFont("Segoe UI", 10))

        self.centralwidget = QtWidgets.QWidget()
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # ===== DATABASE =====
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # ===== MENU =====
        self.menu = QtWidgets.QFrame()
        self.menu.setMaximumWidth(220)
        self.menu.setStyleSheet("background:#2c3e50; border-radius:10px;")

        menu_layout = QtWidgets.QVBoxLayout(self.menu)

        self.toggle_btn = QtWidgets.QPushButton("☰")
        self.toggle_btn.setStyleSheet("color:white; font-size:18px; border:none;")
        menu_layout.addWidget(self.toggle_btn)

        def create_btn(text):
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    background:#34495e;
                    color:white;
                    border-radius:10px;
                    text-align:left;
                    padding-left:10px;
                }
                QPushButton:hover {
                    background:#1abc9c;
                }
            """)
            return btn

        menu_items = {
            "Trang chủ": None,
            "Tạo ticket": self.open_ticket,
            "Kho linh kiện": self.open_kholinhkien,
            "Quản lý khách hàng": self.open_cskh,
            "Đơn đang xử lý": self.open_donxuly,
            "Quản lý nhân sự": self.open_nhansu,
            "Báo cáo - Thống kê": self.open_baocao
        }

        for text, handler in menu_items.items():
            btn = create_btn(text)
            if handler:
                btn.clicked.connect(handler)
            menu_layout.addWidget(btn)

        # ===== CONTENT =====
        content = QtWidgets.QVBoxLayout()

        # HEADER
        header = QtWidgets.QHBoxLayout()

        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(QtGui.QPixmap("C:/Users/tuanc/Downloads/T1_esports_logo.svg.png"))
        self.logo.setFixedSize(140, 60)
        self.logo.setScaledContents(True)

        title = QtWidgets.QLabel("DỊCH VỤ CHĂM SÓC MÁY TÍNH T1")
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        header.addWidget(self.logo)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()

        # MARQUEE
        marquee_container = QtWidgets.QFrame()
        marquee_container.setFixedHeight(30)

        self.marquee = QtWidgets.QLabel(marquee_container)
        self.marquee.setStyleSheet("color:gray; font-style:italic;")

        self.full_text = "Chào mừng quý khách đến với hệ thống quản lý sửa chữa máy tính T1."
        self.marquee.setText(self.full_text)
        self.marquee.adjustSize()

        self.x = marquee_container.width()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.run_text(marquee_container))
        self.timer.start(10)

        # ===== CARDS =====
        card_layout = QtWidgets.QHBoxLayout()

        def create_card(title):
            f = QtWidgets.QFrame()
            f.setStyleSheet("background:white; border-radius:10px; border:1px solid #ddd;")
            l = QtWidgets.QVBoxLayout(f)
            lbl_title = QtWidgets.QLabel(title)
            lbl_value = QtWidgets.QLabel("0")
            lbl_value.setStyleSheet("font-size:18px; color:#2c7be5; font-weight:bold;")
            l.addWidget(lbl_title)
            l.addWidget(lbl_value)
            return f, lbl_value

        self.card_total, self.lbl_total = create_card("Tổng đơn")
        self.card_processing, self.lbl_processing = create_card("Đang xử lý")
        self.card_done, self.lbl_done = create_card("Hoàn thành")

        card_layout.addWidget(self.card_total)
        card_layout.addWidget(self.card_processing)
        card_layout.addWidget(self.card_done)

        # ===== TABLE =====
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Khách", "SĐT", "Lỗi", "Giá tiền", "Ngày"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        content.addLayout(header)
        content.addWidget(marquee_container)
        content.addLayout(card_layout)
        content.addWidget(self.table)

        main_layout.addWidget(self.menu, 1)
        main_layout.addLayout(content, 4)

        # LOAD
        self.load_dashboard()

    # =========================
    def load_dashboard(self):
        query = """
        SELECT t.id_ticket, c.ten, c.sdt, t.loi, t.gia_tien, t.ngay_tao
        FROM ticket t
        JOIN customers c ON t.id_khach = c.id_khach
        ORDER BY t.ngay_tao ASC
        """

        data = self.cursor.execute(query).fetchall()
        self.table.setRowCount(len(data))

        for r, row in enumerate(data):
            for c, val in enumerate(row):

                # 👉 format tiền đẹp
                if c == 4:
                    val = f"{val:,} đ" if val else "0 đ"

                item = QtWidgets.QTableWidgetItem(str(val))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # 🔥 highlight dòng mới nhất
                if r == len(data) - 1:
                    item.setBackground(QtGui.QColor("#e6f7ff"))

                self.table.setItem(r, c, item)

        self.table.scrollToBottom()

        # ===== STATS =====
        total = self.cursor.execute("SELECT COUNT(*) FROM ticket").fetchone()[0]
        done = self.cursor.execute("SELECT COUNT(*) FROM ticket WHERE trang_thai='Hoàn thành'").fetchone()[0]
        processing = self.cursor.execute("SELECT COUNT(*) FROM ticket WHERE trang_thai='Đang xử lý'").fetchone()[0]

        self.lbl_total.setText(str(total))
        self.lbl_done.setText(str(done))
        self.lbl_processing.setText(str(processing))

    # =========================
    def run_text(self, container):
        self.x -= 1
        self.marquee.move(self.x, 5)
        if self.x + self.marquee.width() < 0:
            self.x = container.width()

    # =========================
    def open_ticket(self):
        self.ticket_window = QtWidgets.QMainWindow()
        self.ui_ticket = ticket.Ui_MainWindow()
        self.ui_ticket.setupUi(self.ticket_window)

        # 🔥 realtime update
        self.ui_ticket.ticket_created.connect(self.load_dashboard)

        self.ticket_window.show()

    def open_cskh(self):
        self.cskh_window = cskh.CustomerUI()
        self.cskh_window.show()

    def open_kholinhkien(self):
        self.kho_window = kholinhkien.WarehouseUI()
        self.kho_window.show()

    def open_donxuly(self):
        self.don_window = Donxuly.OrderUI()
        self.don_window.show()

    def open_nhansu(self):
        self.ns_window = Nhansu.StaffUI()
        self.ns_window.show()

    def open_baocao(self):
        self.baocao_window = baocao.ReportUI()
        self.baocao_window.show()


# RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Segoe UI", 10))
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec())