from PyQt6 import QtWidgets, QtGui, QtCore
import sqlite3


class StaffUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý nhân sự")
        self.resize(1100, 650)

        # =========================
        # DATABASE
        # =========================
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # =========================
        # STYLE
        # =========================
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 13px;
                background: #f5f7fb;
            }

            QFrame#card {
                background: white;
                border-radius: 16px;
                border: 1px solid #e5e7eb;
            }

            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                background: white;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2f80ed;
            }

            QPushButton {
                padding: 10px 16px;
                border-radius: 10px;
                font-weight: bold;
                color: white;
            }

            QTableWidget {
                background: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                gridline-color: #f1f5f9;
            }

            QHeaderView::section {
                background: #2f80ed;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }

            QTableWidget::item:selected {
                background: #dbeafe;
                color: black;
            }
        """)

        # =========================
        # MAIN LAYOUT
        # =========================
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # =========================
        # HEADER
        # =========================
        header_layout = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("👨‍💼 QUẢN LÝ NHÂN SỰ")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
        """)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText(
            "🔍 Tìm theo tên, role, SĐT hoặc địa chỉ..."
        )
        self.search_input.setFixedWidth(350)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_input)

        main_layout.addLayout(header_layout)

        # =========================
        # FORM CARD
        # =========================
        form_card = QtWidgets.QFrame()
        form_card.setObjectName("card")

        form_layout = QtWidgets.QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Row 1
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(10)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("👤 Tên nhân viên")

        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems([
            "admin",
            "tiepnhan",
            "ky_thuat"
        ])

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("📞 Số điện thoại")

        row1.addWidget(self.name_input)
        row1.addWidget(self.role_input)
        row1.addWidget(self.phone_input)

        # Row 2
        row2 = QtWidgets.QHBoxLayout()

        self.address_input = QtWidgets.QLineEdit()
        self.address_input.setPlaceholderText("📍 Địa chỉ")

        row2.addWidget(self.address_input)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(10)

        self.add_btn = QtWidgets.QPushButton("➕ Thêm")
        self.add_btn.setStyleSheet("background:#22c55e;")

        self.update_btn = QtWidgets.QPushButton("✏️ Sửa")
        self.update_btn.setStyleSheet("""
            background:#f59e0b;
            color:black;
        """)

        self.delete_btn = QtWidgets.QPushButton("🗑️ Xóa")
        self.delete_btn.setStyleSheet("background:#ef4444;")

        self.clear_btn = QtWidgets.QPushButton("🧹 Làm mới")
        self.clear_btn.setStyleSheet("background:#6b7280;")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        form_layout.addLayout(row1)
        form_layout.addLayout(row2)
        form_layout.addLayout(btn_layout)

        main_layout.addWidget(form_card)

        # =========================
        # TABLE
        # =========================
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên",
            "Vai trò",
            "SĐT",
            "Địa chỉ"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.table.setColumnHidden(0, True)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        main_layout.addWidget(self.table)

        # =========================
        # EVENTS
        # =========================
        self.add_btn.clicked.connect(self.add_staff)
        self.update_btn.clicked.connect(self.update_staff)
        self.delete_btn.clicked.connect(self.delete_staff)
        self.clear_btn.clicked.connect(self.clear_form)
        self.table.cellClicked.connect(self.load_data)
        self.search_input.textChanged.connect(self.search_staff)

        # =========================
        # LOAD DATA
        # =========================
        self.load_staff()

    # =========================
    # LOAD STAFF
    # =========================
    def load_staff(self):
        self.table.setRowCount(0)

        data = self.cursor.execute("""
            SELECT
                id_nv,
                ten,
                role,
                IFNULL(sdt, ''),
                IFNULL(dia_chi, '')
            FROM staff
            ORDER BY id_nv DESC
        """).fetchall()

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, val in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(val))
                item.setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                # Tô màu role
                if col == 2:
                    if val == "admin":
                        item.setBackground(QtGui.QColor("#ef4444"))
                        item.setForeground(QtGui.QColor("white"))

                    elif val == "tiepnhan":
                        item.setBackground(QtGui.QColor("#3b82f6"))
                        item.setForeground(QtGui.QColor("white"))

                    elif val == "ky_thuat":
                        item.setBackground(QtGui.QColor("#f59e0b"))
                        item.setForeground(QtGui.QColor("black"))

                self.table.setItem(row, col, item)

    # =========================
    # ADD STAFF
    # =========================
    def add_staff(self):
        ten = self.name_input.text().strip()
        role = self.role_input.currentText()
        sdt = self.phone_input.text().strip()
        dia_chi = self.address_input.text().strip()

        if not ten:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Vui lòng nhập tên nhân viên!"
            )
            return

        username = ten.replace(" ", "").lower()
        password = "123"

        try:
            self.cursor.execute("""
                INSERT INTO staff
                (
                    ten,
                    username,
                    password,
                    role,
                    sdt,
                    dia_chi
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ten,
                username,
                password,
                role,
                sdt,
                dia_chi
            ))

            self.conn.commit()

            QtWidgets.QMessageBox.information(
                self,
                "Thành công",
                f"Đã thêm nhân viên!\n"
                f"Username: {username}\n"
                f"Password: 123"
            )

            self.load_staff()
            self.clear_form()

        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Username đã tồn tại!"
            )

    # =========================
    # UPDATE STAFF
    # =========================
    def update_staff(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_nv = self.table.item(row, 0).text()

        self.cursor.execute("""
            UPDATE staff
            SET
                ten = ?,
                role = ?,
                sdt = ?,
                dia_chi = ?
            WHERE id_nv = ?
        """, (
            self.name_input.text().strip(),
            self.role_input.currentText(),
            self.phone_input.text().strip(),
            self.address_input.text().strip(),
            id_nv
        ))

        self.conn.commit()
        self.load_staff()
        self.clear_form()

    # =========================
    # DELETE STAFF
    # =========================
    def delete_staff(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_nv = self.table.item(row, 0).text()

        # Xóa trực tiếp, không hiện hộp thoại xác nhận
        self.cursor.execute(
            "DELETE FROM staff WHERE id_nv = ?",
            (id_nv,)
        )

        self.conn.commit()

        # Tải lại dữ liệu
        self.load_staff()

        # Xóa dữ liệu trên form
        self.clear_form()

    # =========================
    # LOAD DATA TO FORM
    # =========================
    def load_data(self, row, column):
        self.name_input.setText(
            self.table.item(row, 1).text()
        )

        self.role_input.setCurrentText(
            self.table.item(row, 2).text()
        )

        self.phone_input.setText(
            self.table.item(row, 3).text()
        )

        self.address_input.setText(
            self.table.item(row, 4).text()
        )

    # =========================
    # CLEAR FORM
    # =========================
    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.role_input.setCurrentIndex(0)

    # =========================
    # SEARCH STAFF
    # =========================
    def search_staff(self):
        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            values = [
                self.table.item(row, col).text().lower()
                for col in range(1, 5)
            ]

            match = any(keyword in value for value in values)
            self.table.setRowHidden(row, not match)

    # =========================
    # CLOSE EVENT
    # =========================
    def closeEvent(self, event):
        try:
            self.conn.close()
        except:
            pass
        event.accept()


# =========================
# RUN TEST
# =========================
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    win = StaffUI()
    win.show()

    sys.exit(app.exec())