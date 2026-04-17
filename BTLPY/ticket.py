from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(700, 550)
        MainWindow.setWindowTitle("Tạo ticket sửa chữa")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # ===== nền =====
        self.centralwidget.setStyleSheet("""
            background-color: #ecf0f3;
        """)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(500)
        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
            }
        """)

        # ===== SHADOW =====
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.card.setGraphicsEffect(shadow)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 20, 30, 20)
        card_layout.setSpacing(15)

        # ===== TITLE =====
        title = QtWidgets.QLabel("🎫 Tạo ticket sửa chữa")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)
        card_layout.addWidget(title)

        # ===== INPUT STYLE =====
        def input_field(placeholder):
            line = QtWidgets.QLineEdit()
            line.setPlaceholderText(placeholder)
            line.setMinimumHeight(35)
            line.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 2px solid #bdc3c7;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border-bottom: 2px solid #3498db;
                }
            """)
            return line

        self.name = input_field("Họ và tên")
        self.contact = input_field("Thông tin liên lạc")
        self.type = input_field("Loại máy")
        self.problem = input_field("Vấn đề")
        self.device = input_field("Tên máy")

        # ===== TEXTAREA =====
        self.desc = QtWidgets.QTextEdit()
        self.desc.setPlaceholderText("Mô tả tình trạng lỗi...")
        self.desc.setFixedHeight(70)
        self.desc.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
            QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        self.extra = input_field("Vật phẩm đi kèm")

        # add vào layout
        for w in [self.name, self.contact, self.type, self.problem, self.device, self.desc, self.extra]:
            card_layout.addWidget(w)

        # ===== BUTTON =====
        btn_layout = QtWidgets.QHBoxLayout()

        self.btn_create = QtWidgets.QPushButton("Tạo ticket")
        self.btn_cancel = QtWidgets.QPushButton("Hủy")

        self.btn_create.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.btn_create.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)

        card_layout.addLayout(btn_layout)

        main_layout.addWidget(self.card)