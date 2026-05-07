from PyQt6 import QtWidgets, QtGui, QtCore
import sqlite3


class WarehouseUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        self.setWindowTitle("Kho linh kiện")

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

        title = QtWidgets.QLabel("📦 KHO LINH KIỆN")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm linh kiện...")

        # ===== FORM =====
        form = QtWidgets.QHBoxLayout()

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Tên linh kiện")

        self.type_input = QtWidgets.QComboBox()
        self.type_input.addItems([
            "RAM",
            "SSD",
            "HDD",
            "Màn hình",
            "Pin",
            "Main"
        ])

        self.qty_input = QtWidgets.QLineEdit()
        self.qty_input.setPlaceholderText("Số lượng")

        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("Giá")

        form.addWidget(self.name_input)
        form.addWidget(self.type_input)
        form.addWidget(self.qty_input)
        form.addWidget(self.price_input)

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

        # ===== TABLE =====
        self.table = QtWidgets.QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên",
            "Loại",
            "Số lượng",
            "Giá"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        main_layout.addWidget(title)
        main_layout.addWidget(self.search_input)
        main_layout.addLayout(form)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.load_data()

        # ===== EVENTS =====
        self.add_btn.clicked.connect(self.add_item)
        self.update_btn.clicked.connect(self.update_item)
        self.delete_btn.clicked.connect(self.delete_item)
        self.clear_btn.clicked.connect(self.clear_form)

        self.table.cellClicked.connect(self.load_row)
        self.search_input.textChanged.connect(self.search)

    # ========================
    # LOAD DATA
    # ========================
    def load_data(self):
        self.table.setRowCount(0)

        query = """
        SELECT id_lk, ten, loai, so_luong, gia
        FROM linhkien
        """

        for row_data in self.cursor.execute(query):

            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, val in enumerate(row_data):

                item = QtWidgets.QTableWidgetItem(str(val))

                item.setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(row, col, item)

    # ========================
    # ADD
    # ========================
    def add_item(self):

        query = """
        INSERT INTO linhkien
        (ten, loai, so_luong, gia)
        VALUES (?, ?, ?, ?)
        """

        values = (
            self.name_input.text(),
            self.type_input.currentText(),
            int(self.qty_input.text()),
            int(self.price_input.text())
        )

        self.cursor.execute(query, values)

        self.conn.commit()

        self.load_data()

        self.clear_form()

    # ========================
    # DELETE
    # ========================
    def delete_item(self):

        row = self.table.currentRow()

        if row < 0:
            return

        id_lk = self.table.item(row, 0).text()

        self.cursor.execute(
            "DELETE FROM linhkien WHERE id_lk=?",
            (id_lk,)
        )

        self.conn.commit()

        self.load_data()

    # ========================
    # UPDATE
    # ========================
    def update_item(self):

        row = self.table.currentRow()

        if row < 0:
            return

        id_lk = self.table.item(row, 0).text()

        query = """
        UPDATE linhkien
        SET ten=?,
            loai=?,
            so_luong=?,
            gia=?
        WHERE id_lk=?
        """

        values = (
            self.name_input.text(),
            self.type_input.currentText(),
            int(self.qty_input.text()),
            int(self.price_input.text()),
            id_lk
        )

        self.cursor.execute(query, values)

        self.conn.commit()

        self.load_data()

    # ========================
    # CLEAR
    # ========================
    def clear_form(self):

        self.name_input.clear()
        self.qty_input.clear()
        self.price_input.clear()

    # ========================
    # LOAD ROW
    # ========================
    def load_row(self, row, col):

        self.name_input.setText(
            self.table.item(row, 1).text()
        )

        self.type_input.setCurrentText(
            self.table.item(row, 2).text()
        )

        self.qty_input.setText(
            self.table.item(row, 3).text()
        )

        self.price_input.setText(
            self.table.item(row, 4).text()
        )

    # ========================
    # SEARCH
    # ========================
    def search(self):

        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):

            name = self.table.item(row, 1).text().lower()

            type_ = self.table.item(row, 2).text().lower()

            match = keyword in name or keyword in type_

            self.table.setRowHidden(row, not match)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    win = WarehouseUI()
    win.resize(1000, 600)
    win.show()

    sys.exit(app.exec())