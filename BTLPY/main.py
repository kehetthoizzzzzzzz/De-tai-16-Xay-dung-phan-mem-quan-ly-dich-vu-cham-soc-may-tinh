import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import ticket   # import file ticket.py
import cskh     # import file cskh.py
import kholinhkien
import Donxuly
import Nhansu
import tracuu
import baocao

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1100, 650)
        MainWindow.setFont(QtGui.QFont("Segoe UI", 10))

        self.centralwidget = QtWidgets.QWidget()
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

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

        # Menu items
        menu_items = {
            "Trang chủ": None,
            "Tạo ticket": self.open_ticket,
            "Kho linh kiện": self.open_kholinhkien,
            "Quản lý khách hàng": self.open_cskh,
            "Đơn đang xử lý": self.open_donxuly,
            "Quản lý nhân sự": self.open_nhansu,
            "Tra cứu sửa chữa": self.open_tracuu,
            "Báo cáo - Thống kê": self.open_baocao
        }

        for text, handler in menu_items.items():
            btn = create_btn(text)
            if handler:
                btn.clicked.connect(handler)
            menu_layout.addWidget(btn)

        # ===== CONTENT =====
        content = QtWidgets.QVBoxLayout()

        # ===== HEADER =====
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

        # ===== MARQUEE =====
        marquee_container = QtWidgets.QFrame()
        marquee_container.setFixedHeight(30)
        marquee_container.setStyleSheet("background:transparent;")

        self.marquee = QtWidgets.QLabel(marquee_container)
        self.marquee.setStyleSheet("color:gray; font-style:italic;")

        self.full_text = "Chào mừng quý khách đã đến với dịch vụ chăm sóc máy tính T1. Chúc quý khách có trải nghiệm vui vẻ, hài lòng."
        self.marquee.setText(self.full_text)
        self.marquee.adjustSize()

        self.x = marquee_container.width()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.run_text(marquee_container))
        self.timer.start(10)

        # ===== CARDS =====
        card_layout = QtWidgets.QHBoxLayout()

        def card(title, value):
            f = QtWidgets.QFrame()
            f.setStyleSheet("background:white; border-radius:10px; border:1px solid #ddd;")
            l = QtWidgets.QVBoxLayout(f)
            l.addWidget(QtWidgets.QLabel(title))
            v = QtWidgets.QLabel(value)
            v.setStyleSheet("font-size:18px; color:#2c7be5; font-weight:bold;")
            l.addWidget(v)
            return f

        card_layout.addWidget(card("Tổng máy", "120"))
        card_layout.addWidget(card("Doanh thu", "5.000.000"))
        card_layout.addWidget(card("CSKH", "15"))
        card_layout.addWidget(card("Hoàn thành", "30"))

        # ===== TABLE =====
        self.table = QtWidgets.QTableWidget(10, 6)
        self.table.setHorizontalHeaderLabels(["Mã", "Khách", "SĐT", "Tình trạng", "Ưu tiên", "Giờ"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        data = [
            ("TK01","Nguyễn Văn A","0901234567","Hỏng màn","Cao","08:30"),
            ("TK02","Trần Văn B","0912345678","Thay bàn phím","Trung bình","09:15"),
            ("TK03","Lê Văn C","0923456789","Không lên nguồn","Cao","10:45"),
            ("TK04","Phạm Văn D","0934567890","Thay pin","Thấp","13:20"),
            ("TK05","Hoàng Văn E","0945678901","Lỗi main","Cao","15:10"),
            ("TK06","Đỗ Văn F","0956789012","Sập nguồn","Cao","08:50"),
            ("TK07","Bùi Văn G","0967890123","Lỗi wifi","Thấp","09:40"),
            ("TK08","Ngô Văn H","0978901234","Lỗi ổ cứng","Trung bình","11:00"),
            ("TK09","Vũ Văn I","0989012345","Nóng máy","Thấp","14:10"),
            ("TK10","Phan Văn K","0990123456","Không nhận sạc","Cao","16:00"),
        ]

        for r, row in enumerate(data):
            for c, val in enumerate(row):
                item = QtWidgets.QTableWidgetItem(val)
                if c == 4:
                    if val == "Cao":
                        item.setBackground(QtGui.QColor("#ff4d4f"))
                        item.setForeground(QtGui.QColor("white"))
                    elif val == "Trung bình":
                        item.setBackground(QtGui.QColor("#faad14"))
                    else:
                        item.setBackground(QtGui.QColor("#52c41a"))
                        item.setForeground(QtGui.QColor("white"))
                self.table.setItem(r, c, item)

        # ===== ADD =====
        content.addLayout(header)
        content.addWidget(marquee_container)
        content.addLayout(card_layout)
        content.addWidget(self.table)

        main_layout.addWidget(self.menu, 1)
        main_layout.addLayout(content, 4)

    def run_text(self, container):
        self.x -= 1
        self.marquee.move(self.x, 5)
        if self.x + self.marquee.width() < 0:
            self.x = container.width()

    # ===== MỞ CÁC WINDOW =====
   
    def open_ticket(self):
        self.ticket_window = QtWidgets.QMainWindow()
        self.ui_ticket = ticket.Ui_MainWindow()
        self.ui_ticket.setupUi(self.ticket_window)
        self.ticket_window.show()

    def open_cskh(self):
        self.cskh_window = cskh.CustomerUI()   # class thực tế trong cskh.py
        self.cskh_window.resize(1000, 600)
        self.cskh_window.show()

    def open_kholinhkien(self):
        self.kho_window = kholinhkien.WarehouseUI()  # class thực tế trong kholinhkien.py
        self.kho_window.resize(1000, 600)
        self.kho_window.show()

    def open_donxuly(self):
        self.don_window = Donxuly.OrderUI()    # class thực tế trong Donxuly.py
        self.don_window.resize(1000, 600)
        self.don_window.show()

    def open_nhansu(self):
        self.ns_window = Nhansu.StaffUI()     # class thực tế trong Nhansu.py
        self.ns_window.resize(1000, 600)
        self.ns_window.show()

    def open_tracuu(self):
        self.tracuu_window = tracuu.LookupUI() # class thực tế trong tracuu.py
        self.tracuu_window.resize(1000, 600)
        self.tracuu_window.show()

    def open_baocao(self):
        self.baocao_window = baocao.ReportUI() # class thực tế trong baocao.py
        self.baocao_window.resize(1000, 600)
        self.baocao_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec())
