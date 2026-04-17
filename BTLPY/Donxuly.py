from PyQt6 import QtWidgets, QtGui, QtCore


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
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
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

        # ===== FORM =====
        form_card = QtWidgets.QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background:white;
                border-radius:12px;
                border:1px solid #ddd;
            }
        """)

        form_layout = QtWidgets.QVBoxLayout(form_card)

        input_layout = QtWidgets.QHBoxLayout()

        self.customer_input = QtWidgets.QLineEdit()
        self.customer_input.setPlaceholderText("👤 Khách")

        self.problem_input = QtWidgets.QLineEdit()
        self.problem_input.setPlaceholderText("💻 Tình trạng máy")

        self.status_input = QtWidgets.QComboBox()
        self.status_input.addItems(["Đang xử lý", "Chờ linh kiện", "Hoàn thành"])

        input_layout.addWidget(self.customer_input)
        input_layout.addWidget(self.problem_input)
        input_layout.addWidget(self.status_input)

        # ===== BUTTON =====
        btn_layout = QtWidgets.QHBoxLayout()

        self.add_btn = QtWidgets.QPushButton("➕ Thêm")
        self.add_btn.setStyleSheet("background:#28a745;")

        self.update_btn = QtWidgets.QPushButton("✏️ Sửa")
        self.update_btn.setStyleSheet("background:#ffc107; color:black;")

        self.delete_btn = QtWidgets.QPushButton("🗑️ Xóa")
        self.delete_btn.setStyleSheet("background:#dc3545;")

        self.clear_btn = QtWidgets.QPushButton("🧹 Clear")
        self.clear_btn.setStyleSheet("background:#6c757d;")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        form_layout.addLayout(input_layout)
        form_layout.addLayout(btn_layout)

        # ===== TABLE =====
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Khách", "Tình trạng", "Trạng thái"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background:#2c7be5;
                color:white;
                padding:6px;
                font-weight:bold;
            }
        """)

        self.table.setAlternatingRowColors(True)

        # ===== ADD =====
        main_layout.addLayout(header)
        main_layout.addWidget(form_card)
        main_layout.addWidget(self.table)

        # ===== EVENTS =====
        self.add_btn.clicked.connect(self.add_order)
        self.update_btn.clicked.connect(self.update_order)
        self.delete_btn.clicked.connect(self.delete_order)
        self.clear_btn.clicked.connect(self.clear_form)
        self.table.cellClicked.connect(self.load_data)
        self.search_input.textChanged.connect(self.search_order)

        # ===== DATA ẢO =====
        self.load_fake_data()

    # ===== DATA =====
    def load_fake_data(self):
        data = [
            ("Nguyễn Văn A", "Hỏng màn", "Đang xử lý"),
            ("Trần Văn B", "Thay bàn phím", "Chờ linh kiện"),
            ("Lê Văn C", "Không lên nguồn", "Đang xử lý"),
            ("Phạm Văn D", "Thay pin", "Hoàn thành"),
        ]

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(value)

                # ===== màu trạng thái =====
                if col == 2:
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

    # ===== FUNCTIONS =====
    def add_order(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        data = [
            self.customer_input.text(),
            self.problem_input.text(),
            self.status_input.currentText()
        ]

        for col, value in enumerate(data):
            item = QtWidgets.QTableWidgetItem(value)

            if col == 2:
                if value == "Đang xử lý":
                    item.setBackground(QtGui.QColor("#faad14"))
                elif value == "Chờ linh kiện":
                    item.setBackground(QtGui.QColor("#1890ff"))
                    item.setForeground(QtGui.QColor("white"))
                elif value == "Hoàn thành":
                    item.setBackground(QtGui.QColor("#52c41a"))
                    item.setForeground(QtGui.QColor("white"))

            self.table.setItem(row, col, item)

    def delete_order(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)

    def update_order(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.customer_input.text()))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(self.problem_input.text()))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(self.status_input.currentText()))

    def clear_form(self):
        self.customer_input.clear()
        self.problem_input.clear()

    def load_data(self, row, column):
        self.customer_input.setText(self.table.item(row, 0).text())
        self.problem_input.setText(self.table.item(row, 1).text())
        self.status_input.setCurrentText(self.table.item(row, 2).text())

    def search_order(self):
        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text().lower()
            status = self.table.item(row, 2).text().lower()

            match = keyword in name or keyword in status
            self.table.setRowHidden(row, not match)


# ===== RUN =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = OrderUI()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())