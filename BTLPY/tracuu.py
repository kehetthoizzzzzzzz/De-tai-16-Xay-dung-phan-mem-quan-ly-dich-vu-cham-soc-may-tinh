from PyQt6 import QtWidgets, QtGui, QtCore


class LookupUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tra cứu sửa chữa")

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
                background: #f5f7fa;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 10px;
                background: white;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 10px;
                background:#2c7be5;
                color:white;
                font-weight:bold;
            }
        """)

        main_layout = QtWidgets.QVBoxLayout(self)

        # ===== TITLE =====
        title = QtWidgets.QLabel("🔍 TRA CỨU SỬA CHỮA")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== SEARCH =====
        search_layout = QtWidgets.QHBoxLayout()

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên hoặc SĐT khách...")

        self.search_btn = QtWidgets.QPushButton("Tra cứu")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        # ===== RESULT TABLE =====
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
        main_layout.addWidget(title)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        # ===== DATA ẢO =====
        self.data = [
            ("Nguyễn Văn A", "0901234567", "Hỏng màn", "Đang xử lý"),
            ("Trần Văn B", "0912345678", "Thay bàn phím", "Chờ linh kiện"),
            ("Lê Văn C", "0923456789", "Không lên nguồn", "Hoàn thành"),
        ]

        # ===== EVENT =====
        self.search_btn.clicked.connect(self.search)
        self.search_input.returnPressed.connect(self.search)

    def search(self):
        keyword = self.search_input.text().lower()

        self.table.setRowCount(0)

        for row_data in self.data:
            name, phone, problem, status = row_data

            if keyword in name.lower() or keyword in phone:
                row = self.table.rowCount()
                self.table.insertRow(row)

                values = [name, problem, status]

                for col, value in enumerate(values):
                    item = QtWidgets.QTableWidgetItem(value)

                    # màu trạng thái
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


# ===== RUN =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = LookupUI()
    win.resize(800, 500)
    win.show()
    sys.exit(app.exec())