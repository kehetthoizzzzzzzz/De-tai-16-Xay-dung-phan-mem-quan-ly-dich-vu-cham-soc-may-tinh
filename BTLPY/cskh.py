from PyQt6 import QtWidgets, QtGui, QtCore


class CustomerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý khách hàng")

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
                background: #f5f7fa;
            }
            QLineEdit {
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

        title = QtWidgets.QLabel("👥 QUẢN LÝ KHÁCH HÀNG")
        title.setStyleSheet("font-size:20px; font-weight:bold;")

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo tên hoặc SĐT...")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_input)

        # ===== FORM CARD =====
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

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("👤 Tên khách")

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("📞 SĐT")

        self.address_input = QtWidgets.QLineEdit()
        self.address_input.setPlaceholderText("🏠 Địa chỉ")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.phone_input)
        input_layout.addWidget(self.address_input)

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
        self.table.setHorizontalHeaderLabels(["Tên", "SĐT", "Địa chỉ"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
                border-radius: 10px;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background:#2c7be5;
                color:white;
                padding:6px;
                border:none;
                font-weight:bold;
            }
            QTableWidget::item:selected {
                background:#1abc9c;
                color:white;
            }
        """)

        self.table.setAlternatingRowColors(True)

        # ===== ADD =====
        main_layout.addLayout(header)
        main_layout.addWidget(form_card)
        main_layout.addWidget(self.table)

        # ===== EVENTS =====
        self.add_btn.clicked.connect(self.add_customer)
        self.update_btn.clicked.connect(self.update_customer)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.clear_btn.clicked.connect(self.clear_form)
        self.table.cellClicked.connect(self.load_data)
        self.search_input.textChanged.connect(self.search_customer)

        # ===== LOAD DATA ẢO =====
        self.load_fake_data()

    # ===== DATA ẢO =====
    def load_fake_data(self):
        data = [
            ("Nguyễn Văn A", "0901234567", "Hà Nội"),
            ("Trần Thị B", "0912345678", "TP.HCM"),
            ("Lê Văn C", "0923456789", "Đà Nẵng"),
            ("Phạm Văn D", "0934567890", "Hải Phòng"),
            ("Hoàng Văn E", "0945678901", "Cần Thơ"),
            ("Đỗ Văn F", "0956789012", "Huế"),
            ("Bùi Văn G", "0967890123", "Bắc Ninh"),
            ("Ngô Văn H", "0978901234", "Nghệ An"),
        ]

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    # ===== FUNCTIONS =====
    def add_customer(self):
        if not self.name_input.text() or not self.phone_input.text():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.name_input.text()))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(self.phone_input.text()))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(self.address_input.text()))

    def delete_customer(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)

    def update_customer(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.name_input.text()))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(self.phone_input.text()))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(self.address_input.text()))

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()

    def load_data(self, row, column):
        self.name_input.setText(self.table.item(row, 0).text())
        self.phone_input.setText(self.table.item(row, 1).text())
        self.address_input.setText(self.table.item(row, 2).text())

    def search_customer(self):
        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text().lower()
            phone = self.table.item(row, 1).text().lower()

            match = keyword in name or keyword in phone
            self.table.setRowHidden(row, not match)


# ===== RUN =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = CustomerUI()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())