from PyQt6 import QtWidgets, QtGui, QtCore
import sqlite3

# MATPLOTLIB
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ReportUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Báo cáo - Thống kê")
        self.resize(1100, 750)

        # =========================
        # KẾT NỐI DATABASE
        # =========================
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # =========================
        # STYLE
        # =========================
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
                background: #f5f7fa;
            }

            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #ddd;
            }

            QTableWidget {
                background: white;
                border-radius: 10px;
                gridline-color: #e5e7eb;
            }

            QHeaderView::section {
                background: #2c7be5;
                color: white;
                padding: 6px;
                font-weight: bold;
                border: none;
            }
        """)

        # =========================
        # LAYOUT CHÍNH
        # =========================
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # =========================
        # TIÊU ĐỀ
        # =========================
        title = QtWidgets.QLabel("📊 BÁO CÁO - THỐNG KÊ")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        """)
        main_layout.addWidget(title)

        # =========================
        # KHU VỰC CARDS
        # =========================
        self.card_layout = QtWidgets.QHBoxLayout()
        self.card_layout.setSpacing(12)

        self.card_total_orders, self.lbl_total_orders = self.create_card(
            "Tổng đơn", "0", "#2c7be5"
        )

        self.card_total_revenue, self.lbl_total_revenue = self.create_card(
            "Doanh thu", "0 VND", "#28a745"
        )

        self.card_done, self.lbl_done = self.create_card(
            "Hoàn thành", "0", "#52c41a"
        )

        self.card_processing, self.lbl_processing = self.create_card(
            "Đang xử lý", "0", "#faad14"
        )

        self.card_waiting, self.lbl_waiting = self.create_card(
            "Chờ linh kiện", "0", "#1890ff"
        )

        self.card_layout.addWidget(self.card_total_orders)
        self.card_layout.addWidget(self.card_total_revenue)
        self.card_layout.addWidget(self.card_done)
        self.card_layout.addWidget(self.card_processing)
        self.card_layout.addWidget(self.card_waiting)

        main_layout.addLayout(self.card_layout)

        # =========================
        # BIỂU ĐỒ
        # =========================
        self.chart_frame = QtWidgets.QFrame()
        chart_layout = QtWidgets.QVBoxLayout(self.chart_frame)

        self.figure = Figure(figsize=(8, 3))
        self.canvas = FigureCanvas(self.figure)

        chart_layout.addWidget(self.canvas)
        main_layout.addWidget(self.chart_frame)

        # =========================
        # BẢNG CHI TIẾT
        # =========================
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Khách hàng",
            "Lỗi",
            "Trạng thái",
            "Chi phí",
            "Ngày tạo"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        main_layout.addWidget(self.table)

        # =========================
        # LOAD DỮ LIỆU
        # =========================
        self.load_report()

    # ==================================================
    # TẠO CARD
    # ==================================================
    def create_card(self, title, value, color):
        frame = QtWidgets.QFrame()
        frame.setMinimumHeight(100)

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(15, 10, 15, 10)

        lbl_title = QtWidgets.QLabel(title)
        lbl_title.setStyleSheet("""
            color: #6b7280;
            font-size: 13px;
        """)

        lbl_value = QtWidgets.QLabel(str(value))
        lbl_value.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {color};
        """)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        layout.addStretch()

        return frame, lbl_value

    # ==================================================
    # VẼ BIỂU ĐỒ
    # ==================================================
    def update_chart(self, done, processing, waiting):
        self.figure.clear()

        ax = self.figure.add_subplot(111)

        labels = [
            "Hoàn thành",
            "Đang xử lý",
            "Chờ linh kiện"
        ]

        values = [
            done,
            processing,
            waiting
        ]

        colors = [
            "#52c41a",
            "#faad14",
            "#1890ff"
        ]

        bars = ax.bar(labels, values, color=colors)

        ax.set_title("Thống kê trạng thái đơn hàng")
        ax.set_ylabel("Số lượng đơn")

        # Hiển thị số trên đầu cột
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(int(height)),
                ha="center",
                va="bottom"
            )

        self.figure.tight_layout()
        self.canvas.draw()

    # ==================================================
    # LOAD DỮ LIỆU BÁO CÁO
    # ==================================================
    def load_report(self):
        try:
            query = """
            SELECT
                t.id_ticket,
                c.ten,
                t.loi,
                IFNULL(t.trang_thai, 'Đang xử lý'),
                IFNULL(t.gia_tien, 0),
                IFNULL(t.ngay_tao, '')
            FROM ticket t
            LEFT JOIN customers c
                ON t.id_khach = c.id_khach
            ORDER BY t.id_ticket DESC
            """

            data = self.cursor.execute(query).fetchall()

            # =========================
            # LOAD TABLE
            # =========================
            self.table.setRowCount(0)

            for row_data in data:
                row = self.table.rowCount()
                self.table.insertRow(row)

                for col, value in enumerate(row_data):
                    if col == 4:
                        value = f"{int(value):,} VND"

                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignCenter
                    )

                    # Tô màu trạng thái
                    if col == 3:
                        status = str(row_data[3])

                        if status == "Đang xử lý":
                            item.setBackground(
                                QtGui.QColor("#faad14")
                            )

                        elif status == "Chờ linh kiện":
                            item.setBackground(
                                QtGui.QColor("#1890ff")
                            )
                            item.setForeground(
                                QtGui.QColor("white")
                            )

                        elif status == "Hoàn thành":
                            item.setBackground(
                                QtGui.QColor("#52c41a")
                            )
                            item.setForeground(
                                QtGui.QColor("white")
                            )

                    self.table.setItem(row, col, item)

            # =========================
            # THỐNG KÊ
            # =========================
            total_orders = len(data)

            # Doanh thu chỉ tính đơn hoàn thành
            total_revenue = sum(
                int(row[4])
                for row in data
                if str(row[3]) == "Hoàn thành"
            )

            done = sum(
                1 for row in data
                if str(row[3]) == "Hoàn thành"
            )

            processing = sum(
                1 for row in data
                if str(row[3]) == "Đang xử lý"
            )

            waiting = sum(
                1 for row in data
                if str(row[3]) == "Chờ linh kiện"
            )

            # =========================
            # HIỂN THỊ CARDS
            # =========================
            self.lbl_total_orders.setText(str(total_orders))
            self.lbl_total_revenue.setText(f"{total_revenue:,} VND")
            self.lbl_done.setText(str(done))
            self.lbl_processing.setText(str(processing))
            self.lbl_waiting.setText(str(waiting))

            # =========================
            # CẬP NHẬT BIỂU ĐỒ
            # =========================
            self.update_chart(done, processing, waiting)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể tải dữ liệu báo cáo:\n{e}"
            )

    # ==================================================
    # ĐÓNG DATABASE
    # ==================================================
    def closeEvent(self, event):
        try:
            self.conn.close()
        except:
            pass
        event.accept()


# ==================================================
# RUN TEST
# ==================================================
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    win = ReportUI()
    win.show()

    sys.exit(app.exec())