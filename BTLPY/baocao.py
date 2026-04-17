from PyQt6 import QtWidgets, QtGui, QtCore


class ReportUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Báo cáo - Thống kê")

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
                background: #f5f7fa;
            }
            QFrame {
                background: white;
                border-radius: 12px;
                border:1px solid #ddd;
            }
        """)

        main_layout = QtWidgets.QVBoxLayout(self)

        # ===== TITLE =====
        title = QtWidgets.QLabel("📊 BÁO CÁO - THỐNG KÊ")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== DATA GIẢ =====
        self.data = [
            ("Nguyễn Văn A", "Hỏng màn", "Đang xử lý", 500000),
            ("Trần Văn B", "Thay bàn phím", "Chờ linh kiện", 300000),
            ("Lê Văn C", "Không lên nguồn", "Hoàn thành", 700000),
            ("Phạm Văn D", "Thay pin", "Hoàn thành", 400000),
            ("Hoàng Văn E", "Lỗi main", "Đang xử lý", 800000),
        ]

        # ===== TÍNH TOÁN =====
        total_orders = len(self.data)
        total_revenue = sum(d[3] for d in self.data)

        done = sum(1 for d in self.data if d[2] == "Hoàn thành")
        processing = sum(1 for d in self.data if d[2] == "Đang xử lý")
        waiting = sum(1 for d in self.data if d[2] == "Chờ linh kiện")

        # ===== CARDS =====
        card_layout = QtWidgets.QHBoxLayout()

        def create_card(title, value, color):
            frame = QtWidgets.QFrame()
            layout = QtWidgets.QVBoxLayout(frame)

            t = QtWidgets.QLabel(title)
            v = QtWidgets.QLabel(str(value))

            v.setStyleSheet(f"font-size:20px; font-weight:bold; color:{color};")

            layout.addWidget(t)
            layout.addWidget(v)

            return frame

        card_layout.addWidget(create_card("Tổng đơn", total_orders, "#2c7be5"))
        card_layout.addWidget(create_card("Doanh thu", f"{total_revenue:,} VND", "#28a745"))
        card_layout.addWidget(create_card("Hoàn thành", done, "#52c41a"))
        card_layout.addWidget(create_card("Đang xử lý", processing, "#faad14"))
        card_layout.addWidget(create_card("Chờ linh kiện", waiting, "#1890ff"))

        # ===== TABLE CHI TIẾT =====
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Khách", "Tình trạng", "Trạng thái", "Chi phí"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet("""
            QTableWidget {
                background:white;
                border-radius:10px;
            }
            QHeaderView::section {
                background:#2c7be5;
                color:white;
                padding:6px;
                font-weight:bold;
            }
        """)

        # ===== LOAD DATA =====
        for row_data in self.data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))

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

        # ===== ADD =====
        main_layout.addWidget(title)
        main_layout.addLayout(card_layout)
        main_layout.addWidget(self.table)


# ===== RUN =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = ReportUI()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())