# =========================
# main.py
# Dashboard chính - Đã sửa:
# 1. Menu bên trái không còn khoảng trống lớn.
# 2. Logo T1 load đúng từ đường dẫn:
#    C:/Users/LEGION/Downloads/T1_esports_logo.svg.png
# =========================

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

    def setupUi(self, MainWindow, role="admin"):
        self.role = role

        # =========================
        # WINDOW
        # =========================
        MainWindow.resize(1366, 768)
        MainWindow.setWindowTitle("Dịch vụ chăm sóc máy tính T1")
        MainWindow.setFont(QtGui.QFont("Segoe UI", 10))

        self.centralwidget = QtWidgets.QWidget()
        MainWindow.setCentralWidget(self.centralwidget)

        # Background toàn bộ cửa sổ
        MainWindow.setStyleSheet("""
            QMainWindow {
                background: #f5f7fb;
            }
        """)

        # Layout chính
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(10)

        # =========================
        # DATABASE
        # =========================
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # =====================================================
        # MENU BÊN TRÁI (FIX KHOẢNG TRỐNG)
        # =====================================================
        self.menu = QtWidgets.QFrame()
        self.menu.setFixedWidth(270)   # cố định chiều rộng
        self.menu.setStyleSheet("""
            QFrame {
                background: #2c3e50;
                border-radius: 15px;
            }
        """)

        menu_layout = QtWidgets.QVBoxLayout(self.menu)
        menu_layout.setContentsMargins(10, 10, 10, 10)
        menu_layout.setSpacing(8)

        # =========================
        # NÚT TOGGLE
        # =========================
        self.toggle_btn = QtWidgets.QPushButton("☰")
        self.toggle_btn.setFixedHeight(34)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 22px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                color: #1abc9c;
            }
        """)
        menu_layout.addWidget(self.toggle_btn)

        # =========================
        # HÀM TẠO BUTTON MENU
        # =========================
        def create_btn(text):
            btn = QtWidgets.QPushButton(text)
            btn.setFixedHeight(58)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

            btn.setStyleSheet("""
                QPushButton {
                    background: #34495e;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 18px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background: #1abc9c;
                }
                QPushButton:pressed {
                    background: #16a085;
                }
            """)
            return btn

        # =========================
        # BUTTONS MENU
        # =========================
        self.btn_home = create_btn("Trang chủ")
        self.btn_ticket = create_btn("Tạo ticket")
        self.btn_kho = create_btn("Kho linh kiện")
        self.btn_khachhang = create_btn("Quản lý khách hàng")
        self.btn_don = create_btn("Đơn đang xử lý")
        self.btn_nhanvien = create_btn("Quản lý nhân sự")
        self.btn_baocao = create_btn("Báo cáo - Thống kê")

        # =========================
        # CONNECT MENU
        # =========================
        self.btn_ticket.clicked.connect(self.open_ticket)
        self.btn_kho.clicked.connect(self.open_kholinhkien)
        self.btn_khachhang.clicked.connect(self.open_cskh)
        self.btn_don.clicked.connect(self.open_donxuly)
        self.btn_nhanvien.clicked.connect(self.open_nhansu)
        self.btn_baocao.clicked.connect(self.open_baocao)

        # =========================
        # THÊM BUTTON VÀO MENU
        # =========================
        buttons = [
            self.btn_home,
            self.btn_ticket,
            self.btn_kho,
            self.btn_khachhang,
            self.btn_don,
            self.btn_nhanvien,
            self.btn_baocao
        ]

        for btn in buttons:
            menu_layout.addWidget(btn)

        # Stretch để đẩy các nút lên trên
        menu_layout.addStretch(1)

        # =====================================================
        # KHU VỰC NỘI DUNG
        # =====================================================
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # =========================
        # HEADER
        # =========================
        header = QtWidgets.QHBoxLayout()

        # LOGO
        self.logo = QtWidgets.QLabel()
        self.logo.setFixedSize(150, 70)

        logo_path = r"C:/Users/LEGION/Downloads/T1_esports_logo.svg.png"
        pixmap = QtGui.QPixmap(logo_path)

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    150,
                    70,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            self.logo.setText("T1")
            self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.logo.setStyleSheet("""
                color: red;
                font-size: 28px;
                font-weight: bold;
            """)

        # TIÊU ĐỀ
        title = QtWidgets.QLabel("DỊCH VỤ CHĂM SÓC MÁY TÍNH T1")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
        """)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        header.addWidget(self.logo)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()

        # =========================
        # MARQUEE
        # =========================
        marquee_container = QtWidgets.QFrame()
        marquee_container.setFixedHeight(30)
        marquee_container.setStyleSheet("background: transparent;")

        self.marquee = QtWidgets.QLabel(marquee_container)
        self.marquee.setStyleSheet("""
            color: gray;
            font-style: italic;
            font-size: 11pt;
        """)

        self.full_text = (
            "Chào mừng quý khách đến với hệ thống quản lý sửa chữa máy tính T1."
        )
        self.marquee.setText(self.full_text)
        self.marquee.adjustSize()

        self.x = 1000
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.run_text(marquee_container))
        self.timer.start(10)

        # =========================
        # THẺ THỐNG KÊ
        # =========================
        card_layout = QtWidgets.QHBoxLayout()
        card_layout.setSpacing(12)

        def create_card(title_text):
            frame = QtWidgets.QFrame()
            frame.setFixedHeight(85)
            frame.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 1px solid #dfe3e8;
                    border-radius: 12px;
                }
            """)

            layout = QtWidgets.QVBoxLayout(frame)
            layout.setContentsMargins(14, 10, 14, 10)

            lbl_title = QtWidgets.QLabel(title_text)
            lbl_title.setStyleSheet("""
                font-size: 11pt;
                color: #555;
            """)

            lbl_value = QtWidgets.QLabel("0")
            lbl_value.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #2c7be5;
            """)

            layout.addWidget(lbl_title)
            layout.addWidget(lbl_value)

            return frame, lbl_value

        self.card_total, self.lbl_total = create_card("Tổng đơn")
        self.card_processing, self.lbl_processing = create_card("Đang xử lý")
        self.card_done, self.lbl_done = create_card("Hoàn thành")

        card_layout.addWidget(self.card_total)
        card_layout.addWidget(self.card_processing)
        card_layout.addWidget(self.card_done)

        # =========================
        # TABLE
        # =========================
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Khách",
            "SĐT",
            "Lỗi",
            "Giá tiền",
            "Ngày"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #dfe3e8;
                border-radius: 12px;
                gridline-color: #e5e7eb;
            }
            QHeaderView::section {
                background: #f3f4f6;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # =========================
        # THÊM VÀO CONTENT
        # =========================
        content_layout.addLayout(header)
        content_layout.addWidget(marquee_container)
        content_layout.addLayout(card_layout)
        content_layout.addWidget(self.table)

        # =========================
        # THÊM VÀO MAIN LAYOUT
        # =========================
        main_layout.addWidget(self.menu)
        main_layout.addLayout(content_layout, 1)

        # =========================
        # ROLE
        # =========================
        if role == "tiepnhan":
            self.btn_kho.hide()
            self.btn_nhanvien.hide()
            self.btn_baocao.hide()

        elif role == "ky_thuat":
            self.btn_ticket.hide()
            self.btn_khachhang.hide()
            self.btn_nhanvien.hide()
            self.btn_baocao.hide()

        # =========================
        # LOAD DỮ LIỆU
        # =========================
        self.load_dashboard()

    # =====================================================
    # LOAD DASHBOARD
    # =====================================================
    def load_dashboard(self):
        try:
            query = """
                SELECT
                    t.id_ticket,
                    c.ten,
                    c.sdt,
                    t.loi,
                    t.gia_tien,
                    t.ngay_tao
                FROM ticket t
                JOIN customers c
                    ON t.id_khach = c.id_khach
                ORDER BY t.ngay_tao ASC
            """

            data = self.cursor.execute(query).fetchall()
            self.table.setRowCount(len(data))

            for r, row in enumerate(data):
                for c, val in enumerate(row):
                    if c == 4:
                        val = f"{val:,} đ" if val else "0 đ"

                    item = QtWidgets.QTableWidgetItem(str(val))
                    item.setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignCenter
                    )

                    if r == len(data) - 1:
                        item.setBackground(QtGui.QColor("#e6f7ff"))

                    self.table.setItem(r, c, item)

            self.table.scrollToBottom()

            # Thống kê
            total = self.cursor.execute(
                "SELECT COUNT(*) FROM ticket"
            ).fetchone()[0]

            done = self.cursor.execute(
                "SELECT COUNT(*) FROM ticket "
                "WHERE trang_thai='Hoàn thành'"
            ).fetchone()[0]

            processing = self.cursor.execute(
                "SELECT COUNT(*) FROM ticket "
                "WHERE trang_thai='Đang xử lý'"
            ).fetchone()[0]

            self.lbl_total.setText(str(total))
            self.lbl_done.setText(str(done))
            self.lbl_processing.setText(str(processing))

        except Exception as e:
            print("Lỗi load dashboard:", e)

    # =====================================================
    # CHẠY CHỮ
    # =====================================================
    def run_text(self, container):
        self.x -= 1
        self.marquee.move(self.x, 5)

        if self.x + self.marquee.width() < 0:
            self.x = container.width()

    # =====================================================
    # MỞ CÁC CỬA SỔ
    # =====================================================
    def open_ticket(self):
        self.ticket_window = QtWidgets.QMainWindow()
        self.ui_ticket = ticket.Ui_MainWindow()
        self.ui_ticket.setupUi(self.ticket_window)
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


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Segoe UI", 10))

    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)

    win.show()
    sys.exit(app.exec())