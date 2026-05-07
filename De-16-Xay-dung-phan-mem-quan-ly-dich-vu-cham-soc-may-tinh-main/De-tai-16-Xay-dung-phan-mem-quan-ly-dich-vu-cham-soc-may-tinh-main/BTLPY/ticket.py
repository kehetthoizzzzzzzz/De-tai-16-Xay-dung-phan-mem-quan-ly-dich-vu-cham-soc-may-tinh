from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
import sqlite3


class Ui_MainWindow(QtCore.QObject):

    ticket_created = QtCore.pyqtSignal()

    def setupUi(self, MainWindow):

        super().__init__()

        MainWindow.resize(700, 650)
        MainWindow.setWindowTitle("Tạo ticket sửa chữa")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("""
            background-color: #ecf0f3;
        """)

        main_layout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )

        main_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # ========================
        # CARD
        # ========================
        self.card = QtWidgets.QFrame()

        self.card.setFixedWidth(520)

        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
            }
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect()

        shadow.setBlurRadius(25)
        shadow.setYOffset(5)

        shadow.setColor(
            QtGui.QColor(0, 0, 0, 80)
        )

        self.card.setGraphicsEffect(shadow)

        card_layout = QtWidgets.QVBoxLayout(
            self.card
        )

        card_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        card_layout.setSpacing(12)

        # ========================
        # TITLE
        # ========================
        title = QtWidgets.QLabel(
            "🎫 Tạo ticket sửa chữa"
        )

        title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)

        card_layout.addWidget(title)

        # ========================
        # INPUT STYLE
        # ========================
        def input_field(placeholder):

            line = QtWidgets.QLineEdit()

            line.setPlaceholderText(
                placeholder
            )

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

            # FIX PLACEHOLDER
            cb.setCurrentIndex(-1)

            cb.lineEdit().setPlaceholderText(
                placeholder
            )

            cb.lineEdit().setAlignment(
                QtCore.Qt.AlignmentFlag.AlignLeft
            )

            return cb

        # ========================
        # KHÁCH HÀNG
        # ========================
        self.cb_khach = combo_box(
            "Chọn khách hàng"
        )

        self.cb_khach.setInsertPolicy(
            QtWidgets.QComboBox.InsertPolicy.NoInsert
        )

        completer_khach = QtWidgets.QCompleter(
            self.cb_khach.model(),
            self.cb_khach
        )

        completer_khach.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )

        completer_khach.setFilterMode(
            QtCore.Qt.MatchFlag.MatchContains
        )

        self.cb_khach.setCompleter(
            completer_khach
        )

        # ========================
        # NHÂN VIÊN
        # ========================
        self.cb_nv = combo_box(
            "Chọn nhân viên xử lý"
        )

        self.cb_nv.setInsertPolicy(
            QtWidgets.QComboBox.InsertPolicy.NoInsert
        )

        completer_nv = QtWidgets.QCompleter(
            self.cb_nv.model(),
            self.cb_nv
        )

        completer_nv.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )

        completer_nv.setFilterMode(
            QtCore.Qt.MatchFlag.MatchContains
        )

        self.cb_nv.setCompleter(
            completer_nv
        )

        # ========================
        # LOẠI MÁY
        # ========================
        self.type = combo_box(
            "Chọn loại máy"
        )

        self.type.addItems([
            "Laptop",
            "PC - Máy bàn",
            "Điện thoại",
            "Máy tính bảng",
            "Máy in",
            "Khác"
        ])

        self.type.setCurrentIndex(-1)

        # ========================
        # LINH KIỆN
        # ========================
        self.cb_linhkien = combo_box(
            "Chọn linh kiện"
        )

        self.sl_linhkien = input_field(
            "Số lượng"
        )

        self.sl_linhkien.setValidator(
            QIntValidator(1, 9999)
        )

        self.btn_add_lk = QtWidgets.QPushButton(
            "➕ Thêm linh kiện"
        )

        self.btn_add_lk.setStyleSheet("""
            background:#27ae60;
            color:white;
            padding:8px;
            border-radius:8px;
        """)

        # ========================
        # TABLE LINH KIỆN
        # ========================
        self.table_lk = QtWidgets.QTableWidget(
            0,
            4
        )

        self.table_lk.setHorizontalHeaderLabels([
            "Linh kiện",
            "SL",
            "Đơn giá",
            "Thành tiền"
        ])

        self.table_lk.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.table_lk.setFixedHeight(130)

        # ========================
        # THÔNG TIN MÁY
        # ========================
        self.problem = input_field(
            "Vấn đề"
        )

        self.device = input_field(
            "Tên máy"
        )

        self.desc = QtWidgets.QTextEdit()

        self.desc.setPlaceholderText(
            "Mô tả tình trạng lỗi..."
        )

        self.desc.setFixedHeight(70)

        # ========================
        # GIÁ
        # ========================
        self.gia = input_field(
            "Nhập tiền công sửa chữa"
        )

        self.gia.setValidator(
            QIntValidator(0, 1000000000)
        )

        # ========================
        # TOTAL
        # ========================
        self.lb_total = QtWidgets.QLabel(
            "Tổng linh kiện: 0 VND"
        )

        self.lb_total.setStyleSheet("""
            font-weight:bold;
            color:#e67e22;
            font-size:14px;
        """)

        # ========================
        # ADD WIDGET
        # ========================
        for w in [
            self.cb_khach,
            self.cb_nv,
            self.type,

            self.cb_linhkien,
            self.sl_linhkien,
            self.btn_add_lk,

            self.table_lk,
            self.lb_total,

            self.problem,
            self.device,
            self.desc,
            self.gia
        ]:
            card_layout.addWidget(w)

        # ========================
        # BUTTON
        # ========================
        btn_layout = QtWidgets.QHBoxLayout()

        self.btn_create = QtWidgets.QPushButton(
            "Tạo ticket"
        )

        self.btn_cancel = QtWidgets.QPushButton(
            "Hủy"
        )

        self.btn_create.setStyleSheet("""
            background:#3498db;
            color:white;
            padding:10px;
            border-radius:8px;
        """)

        self.btn_cancel.setStyleSheet("""
            background:#e74c3c;
            color:white;
            padding:10px;
            border-radius:8px;
        """)

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)

        card_layout.addLayout(btn_layout)

        main_layout.addWidget(self.card)

        # ========================
        # INIT DB
        # ========================
        self.init_db()

        self.load_khach()
        self.load_nv()
        self.load_linhkien()

        # ========================
        # EVENTS
        # ========================
        self.btn_create.clicked.connect(
            self.create_ticket
        )

        self.btn_cancel.clicked.connect(
            MainWindow.close
        )

        self.btn_add_lk.clicked.connect(
            self.add_linhkien
        )

    # ========================
    # DATABASE
    # ========================
    def init_db(self):

        self.conn = sqlite3.connect(
            "data.db"
        )

        self.cursor = self.conn.cursor()

    # ========================
    # LOAD KHÁCH
    # ========================
    def load_khach(self):

        self.cb_khach.clear()

        for row in self.cursor.execute(
            "SELECT id_khach, ten FROM customers"
        ):

            self.cb_khach.addItem(
                row[1],
                row[0]
            )

        self.cb_khach.setCurrentIndex(-1)

    # ========================
    # LOAD NHÂN VIÊN
    # ========================
    def load_nv(self):

        self.cb_nv.clear()

        for row in self.cursor.execute(
            "SELECT id_nv, ten FROM staff"
        ):

            self.cb_nv.addItem(
                row[1],
                row[0]
            )

        self.cb_nv.setCurrentIndex(-1)

    # ========================
    # LOAD LINH KIỆN
    # ========================
    def load_linhkien(self):

        self.cb_linhkien.clear()

        query = """
        SELECT id_lk, ten, so_luong
        FROM linhkien
        """

        for row in self.cursor.execute(query):

            text = f"{row[1]} (còn {row[2]})"

            self.cb_linhkien.addItem(
                text,
                row[0]
            )

        self.cb_linhkien.setCurrentIndex(-1)

    # ========================
    # UPDATE TOTAL
    # ========================
    def update_total(self):

        total = 0

        for row in range(
            self.table_lk.rowCount()
        ):

            thanh_tien = int(
                self.table_lk.item(
                    row,
                    3
                ).text()
            )

            total += thanh_tien

        self.lb_total.setText(
            f"Tổng linh kiện: {total:,} VND"
        )

    # ========================
    # ADD LINH KIỆN
    # ========================
    def add_linhkien(self):

        id_lk = self.cb_linhkien.currentData()

        sl_text = self.sl_linhkien.text()

        if not sl_text:

            QtWidgets.QMessageBox.warning(
                None,
                "Lỗi",
                "Nhập số lượng!"
            )

            return

        sl = int(sl_text)

        self.cursor.execute("""
        SELECT ten, so_luong, gia
        FROM linhkien
        WHERE id_lk=?
        """, (id_lk,))

        result = self.cursor.fetchone()

        if not result:
            return

        ten = result[0]
        ton_kho = result[1]
        don_gia = result[2]

        if sl > ton_kho:

            QtWidgets.QMessageBox.warning(
                None,
                "Lỗi",
                f"Tồn kho chỉ còn {ton_kho}!"
            )

            return

        thanh_tien = don_gia * sl

        row = self.table_lk.rowCount()

        self.table_lk.insertRow(row)

        self.table_lk.setItem(
            row,
            0,
            QtWidgets.QTableWidgetItem(ten)
        )

        self.table_lk.setItem(
            row,
            1,
            QtWidgets.QTableWidgetItem(str(sl))
        )

        self.table_lk.setItem(
            row,
            2,
            QtWidgets.QTableWidgetItem(str(don_gia))
        )

        self.table_lk.setItem(
            row,
            3,
            QtWidgets.QTableWidgetItem(str(thanh_tien))
        )

        self.update_total()

        self.sl_linhkien.clear()

    # ========================
    # CREATE TICKET
    # ========================
    def create_ticket(self):

        idx_khach = self.cb_khach.findText(
            self.cb_khach.currentText()
        )

        id_khach = (
            self.cb_khach.itemData(idx_khach)
            if idx_khach != -1 else None
        )

        idx_nv = self.cb_nv.findText(
            self.cb_nv.currentText()
        )

        id_nv = (
            self.cb_nv.itemData(idx_nv)
            if idx_nv != -1 else None
        )

        loai = self.type.currentText()

        loi = self.problem.text()

        tenmay = self.device.text()

        mota = self.desc.toPlainText()

        gia = self.gia.text()

        # ===== CHECK =====
        if not id_khach or not id_nv:

            QtWidgets.QMessageBox.warning(
                None,
                "Lỗi",
                "Chọn khách và nhân viên!"
            )

            return

        if not loai:

            QtWidgets.QMessageBox.warning(
                None,
                "Lỗi",
                "Chọn loại máy!"
            )

            return

        if not gia:

            QtWidgets.QMessageBox.warning(
                None,
                "Lỗi",
                "Nhập tiền công!"
            )

            return

        tien_cong = int(gia)

        # ===== TỔNG LINH KIỆN =====
        tong_linh_kien = 0

        for row in range(
            self.table_lk.rowCount()
        ):

            thanh_tien = int(
                self.table_lk.item(
                    row,
                    3
                ).text()
            )

            tong_linh_kien += thanh_tien

        tong_tien = tien_cong + tong_linh_kien

        # ===== INSERT TICKET =====
        query = """
        INSERT INTO ticket
        (
            id_khach,
            id_nv,
            loai_may,
            loi,
            ten_may,
            mo_ta,
            gia_tien
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(query, (
            id_khach,
            id_nv,
            loai,
            loi,
            tenmay,
            mota,
            tong_tien
        ))

        id_ticket = self.cursor.lastrowid

        # ===== LƯU LINH KIỆN =====
        for row in range(
            self.table_lk.rowCount()
        ):

            ten_lk = self.table_lk.item(
                row,
                0
            ).text()

            sl = int(
                self.table_lk.item(
                    row,
                    1
                ).text()
            )

            thanh_tien = int(
                self.table_lk.item(
                    row,
                    3
                ).text()
            )

            self.cursor.execute("""
            SELECT id_lk
            FROM linhkien
            WHERE ten=?
            """, (ten_lk,))

            id_lk = self.cursor.fetchone()[0]

            self.cursor.execute("""
            INSERT INTO ticket_linhkien
            (
                id_ticket,
                id_lk,
                so_luong,
                gia
            )
            VALUES (?, ?, ?, ?)
            """, (
                id_ticket,
                id_lk,
                sl,
                thanh_tien
            ))

            self.cursor.execute("""
            UPDATE linhkien
            SET so_luong = so_luong - ?
            WHERE id_lk=?
            """, (
                sl,
                id_lk
            ))

        self.conn.commit()

        QtWidgets.QMessageBox.information(
            None,
            "Thành công",
            f"Đã tạo ticket!\n\n"
            f"Tiền công: {tien_cong:,} VND\n"
            f"Linh kiện: {tong_linh_kien:,} VND\n"
            f"Tổng thanh toán: {tong_tien:,} VND"
        )

        self.ticket_created.emit()

        # ===== RESET =====
        self.cb_khach.setCurrentIndex(-1)

        self.cb_nv.setCurrentIndex(-1)

        self.type.setCurrentIndex(-1)

        self.problem.clear()

        self.device.clear()

        self.desc.clear()

        self.gia.clear()

        self.sl_linhkien.clear()

        self.table_lk.setRowCount(0)

        self.update_total()

        self.load_linhkien()


# ========================
# RUN
# ========================
if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec())