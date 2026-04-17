import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

class ModernTicketApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hệ thống tạo Ticket - Repair Service")
        self.resize(700, 800)
        self.setStyleSheet("background-color: #f0f2f5;")  # Màu nền xám nhạt hiện đại

        # --- WIDGET CHÍNH & LAYOUT TỔNG ---
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(40, 40, 40, 40) # Tạo khoảng trống lề
        self.main_layout.setSpacing(20)

        # --- KHUNG THẺ (CARD VIEW) ---
        self.card_frame = QtWidgets.QFrame()
        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Hiệu ứng đổ bóng cho khung thẻ
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
        self.card_frame.setGraphicsEffect(shadow)

        self.card_layout = QtWidgets.QVBoxLayout(self.card_frame)
        self.card_layout.setContentsMargins(30, 30, 30, 30)
        self.card_layout.setSpacing(15)

        # --- TIÊU ĐỀ ---
        self.label_title = QtWidgets.QLabel("TẠO TICKET SỬA CHỮA")
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1a73e8;
            margin-bottom: 10px;
        """)
        self.card_layout.addWidget(self.label_title)

        # --- FORM LAYOUT (CHIA CỘT NHÃN & Ô NHẬP) ---
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.form_layout.setSpacing(12)

        # QSS cho các ô nhập liệu
        input_style = """
            QTextEdit, QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                background-color: #fafafa;
                font-size: 14px;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #1a73e8;
                background-color: white;
            }
        """

        # Danh sách các trường cần tạo
        self.inputs = {}
        fields = [
            ("Họ và tên:", "name"),
            ("Thông tin liên lạc:", "contact"),
            ("Loại máy:", "type"),
            ("Tên máy:", "model"),
            ("Vấn đề cần xử lý:", "issue"),
            ("Mô tả tình trạng:", "desc"),
            ("Vật phẩm đi kèm:", "items")
        ]

        for label_text, key in fields:
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet("font-weight: 600; color: #555; font-size: 14px;")
            
            # Sử dụng QTextEdit cho các trường mô tả dài, QLineEdit cho trường ngắn
            if key in ["desc", "items"]:
                edit = QtWidgets.QTextEdit()
                edit.setMaximumHeight(80)
            else:
                edit = QtWidgets.QLineEdit()
            
            edit.setStyleSheet(input_style)
            self.form_layout.addRow(lbl, edit)
            self.inputs[key] = edit

        self.card_layout.addLayout(self.form_layout)

        # --- NÚT BẤM (BUTTONS) ---
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(15)
        self.button_layout.addStretch() # Đẩy nút sang bên phải

        self.btn_cancel = QtWidgets.QPushButton("Hủy bỏ")
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f1f3f4;
                color: #5f6368;
                border-radius: 8px;
                padding: 10px 25px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e8eaed;
            }
        """)

        self.btn_submit = QtWidgets.QPushButton("Tạo Ticket")
        self.btn_submit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border-radius: 8px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)

        self.button_layout.addWidget(self.btn_cancel)
        self.button_layout.addWidget(self.btn_submit)
        self.card_layout.addLayout(self.button_layout)

        # Thêm Card vào Main Layout
        self.main_layout.addWidget(self.card_frame)
        self.main_layout.addStretch() # Đảm bảo card không bị kéo dãn quá mức theo chiều dọc

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Font hệ thống hiện đại
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernTicketApp()
    window.show()
    sys.exit(app.exec())