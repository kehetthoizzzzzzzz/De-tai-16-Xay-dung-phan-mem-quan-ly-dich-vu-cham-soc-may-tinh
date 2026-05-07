from PyQt6 import QtWidgets, QtGui, QtCore
import sqlite3


class StaffUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý nhân sự")

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

        # ===== DB =====
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        main_layout = QtWidgets.QVBoxLayout(self)

        # ===== HEADER =====
        header = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("👨‍💼 QUẢN LÝ NHÂN SỰ")
        title.setStyleSheet("font-size:20px; font-weight:bold;")

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo tên hoặc role...")

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

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("👤 Tên nhân viên")

        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["admin", "staff"])

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("📞 SĐT")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.role_input)
        input_layout.addWidget(self.phone_input)

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
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Role", "SĐT"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setColumnHidden(0, True)

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
        self.add_btn.clicked.connect(self.add_staff)
        self.update_btn.clicked.connect(self.update_staff)
        self.delete_btn.clicked.connect(self.delete_staff)
        self.clear_btn.clicked.connect(self.clear_form)
        self.table.cellClicked.connect(self.load_data)
        self.search_input.textChanged.connect(self.search_staff)

        # ===== LOAD =====
        self.load_staff()

    # =========================
    def load_staff(self):
        self.table.setRowCount(0)

        data = self.cursor.execute("""
            SELECT id_nv, ten, role, sdt
            FROM staff
            ORDER BY id_nv DESC
        """).fetchall()

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, val in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(val))

                # màu role
                if col == 2:
                    if val == "admin":
                        item.setBackground(QtGui.QColor("#ff4d4f"))
                        item.setForeground(QtGui.QColor("white"))
                    else:
                        item.setBackground(QtGui.QColor("#52c41a"))
                        item.setForeground(QtGui.QColor("white"))

                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    # =========================
    def add_staff(self):
        ten = self.name_input.text()
        role = self.role_input.currentText()
        sdt = self.phone_input.text()

        if not ten:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Nhập tên!")
            return

        username = ten.replace(" ", "").lower()
        password = "123"

        try:
            self.cursor.execute("""
            INSERT INTO staff (ten, username, password, role, sdt)
            VALUES (?, ?, ?, ?, ?)
            """, (ten, username, password, role, sdt))

            self.conn.commit()
            self.load_staff()
            self.clear_form()

        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Username bị trùng!")

    # =========================
    def update_staff(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_nv = self.table.item(row, 0).text()

        self.cursor.execute("""
        UPDATE staff
        SET ten=?, role=?, sdt=?
        WHERE id_nv=?
        """, (
            self.name_input.text(),
            self.role_input.currentText(),
            self.phone_input.text(),
            id_nv
        ))

        self.conn.commit()
        self.load_staff()

    # =========================
    def delete_staff(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_nv = self.table.item(row, 0).text()

        self.cursor.execute("DELETE FROM staff WHERE id_nv=?", (id_nv,))
        self.conn.commit()
        self.load_staff()

    # =========================
    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.role_input.setCurrentIndex(0)

    # =========================
    def load_data(self, row, column):
        self.name_input.setText(self.table.item(row, 1).text())
        self.role_input.setCurrentText(self.table.item(row, 2).text())
        self.phone_input.setText(self.table.item(row, 3).text())

    # =========================
    def search_staff(self):
        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower()
            role = self.table.item(row, 2).text().lower()

            match = keyword in name or keyword in role
            self.table.setRowHidden(row, not match)


# ===== RUN =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = StaffUI()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())