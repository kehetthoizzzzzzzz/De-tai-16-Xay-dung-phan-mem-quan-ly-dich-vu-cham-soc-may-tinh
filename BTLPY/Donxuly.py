from PyQt6 import QtWidgets, QtGui, QtCore
import sqlite3


class OrderUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Đơn đang xử lý")

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
                background: #f5f7fa;
            }
        """)

        main_layout = QtWidgets.QVBoxLayout(self)

        # ===== HEADER =====
        header = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("🛠️ ĐƠN ĐANG XỬ LÝ")
        title.setStyleSheet("font-size:20px; font-weight:bold;")

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo khách / trạng thái...")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_input)

        # ===== BUTTON =====
        btn_layout = QtWidgets.QHBoxLayout()

        self.btn_done = QtWidgets.QPushButton("✅ Hoàn thành đơn")
        self.btn_done.setStyleSheet("""
            QPushButton {
                background:#52c41a;
                color:white;
                padding:8px;
                border-radius:8px;
            }
        """)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_done)

        # ===== TABLE =====
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Khách", "Lỗi", "Giá tiền", "Trạng thái"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)

        self.table.setAlternatingRowColors(True)

        # ===== ADD =====
        main_layout.addLayout(header)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        # ===== DB =====
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # ===== EVENT =====
        self.search_input.textChanged.connect(self.search_order)
        self.table.cellDoubleClicked.connect(self.show_detail)
        self.btn_done.clicked.connect(self.mark_done)

        # ===== AUTO REFRESH =====
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load_ticket)
        self.timer.start(3000)  # 3s reload

        self.load_ticket()

    # =========================
    def load_ticket(self):
        self.table.setRowCount(0)

        query = """
        SELECT t.id_ticket, c.ten, t.loi, t.gia_tien, t.trang_thai
        FROM ticket t
        JOIN customers c ON t.id_khach = c.id_khach
        ORDER BY t.ngay_tao ASC
        """

        for row_data in self.cursor.execute(query):
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(row_data):

                if col == 3:
                    value = f"{value:,} đ" if value else "0 đ"

                item = QtWidgets.QTableWidgetItem(str(value))

                # màu trạng thái
                if col == 4:
                    if value == "Đang xử lý":
                        item.setBackground(QtGui.QColor("#faad14"))
                    elif value == "Chờ linh kiện":
                        item.setBackground(QtGui.QColor("#1890ff"))
                        item.setForeground(QtGui.QColor("white"))
                    elif value == "Hoàn thành":
                        item.setBackground(QtGui.QColor("#52c41a"))
                        item.setForeground(QtGui.QColor("white"))

                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        self.table.scrollToBottom()

    # =========================
    def mark_done(self):
        row = self.table.currentRow()

        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chọn 1 đơn!")
            return

        status = self.table.item(row, 4).text()
        if status == "Hoàn thành":
            QtWidgets.QMessageBox.information(self, "Thông báo", "Đã hoàn thành rồi!")
            return

        id_ticket = self.table.item(row, 0).text()

        self.cursor.execute(
            "UPDATE ticket SET trang_thai='Hoàn thành' WHERE id_ticket=?",
            (id_ticket,)
        )
        self.conn.commit()

        QtWidgets.QMessageBox.information(self, "OK", "Đã hoàn thành!")

        self.load_ticket()

    # =========================
    def search_order(self):
        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower()
            status = self.table.item(row, 4).text().lower()

            self.table.setRowHidden(row, not (keyword in name or keyword in status))

    # =========================
    def show_detail(self, row, column):
        id_ticket = self.table.item(row, 0).text()

        query = """
        SELECT t.id_ticket, c.ten, c.sdt, s.ten,
               t.loai_may, t.loi, t.ten_may,
               t.mo_ta, t.gia_tien,
               t.trang_thai, t.ngay_tao
        FROM ticket t
        JOIN customers c ON t.id_khach = c.id_khach
        LEFT JOIN staff s ON t.id_nv = s.id_nv
        WHERE t.id_ticket = ?
        """

        result = self.cursor.execute(query, (id_ticket,)).fetchone()

        if not result:
            return

        staff_name = result[3] if result[3] else "Chưa phân công"

        QtWidgets.QMessageBox.information(self, "Chi tiết", f"""
🎫 ID: {result[0]}

👤 Khách: {result[1]}
📞 SĐT: {result[2]}
👨‍🔧 NV: {staff_name}

💻 Loại máy: {result[4]}
⚠️ Lỗi: {result[5]}
🖥️ Máy: {result[6]}

📝 Mô tả:
{result[7]}

💰 Giá: {result[8]:,} đ

📊 Trạng thái: {result[9]}
📅 Ngày: {result[10]}
""")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = OrderUI()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())