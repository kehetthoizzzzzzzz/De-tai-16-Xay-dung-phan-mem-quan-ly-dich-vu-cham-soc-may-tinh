import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # ========================
    # TABLE customers
    # ========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id_khach INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        sdt TEXT,
        dia_chi TEXT
    )
    """)

    # ========================
    # TABLE staff
    # ========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id_nv INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        sdt TEXT
    )
    """)

    # ========================
    # TABLE ticket (QUAN TRỌNG)
    # ========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket (
        id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
        id_khach INTEGER NOT NULL,
        id_nv INTEGER,

        loai_may TEXT,
        loi TEXT,
        ten_may TEXT,
        mo_ta TEXT,

        gia_tien INTEGER DEFAULT 0,

        trang_thai TEXT DEFAULT 'Đang xử lý',

        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_khach) REFERENCES customers(id_khach) ON DELETE CASCADE,
        FOREIGN KEY (id_nv) REFERENCES staff(id_nv) ON DELETE SET NULL
    )
    """)

    # ========================
    # TABLE logs
    # ========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ticket INTEGER,
        hanh_dong TEXT,
        thoi_gian DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket) ON DELETE CASCADE
    )
    """)

    # ========================
    # SAMPLE DATA
    # ========================
    cursor.execute("SELECT COUNT(*) FROM staff")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO staff (ten, username, password, role, sdt)
        VALUES (?, ?, ?, ?, ?)
        """, [
            ("Admin", "admin", "123", "admin", "0900000000"),
            ("Kỹ thuật 1", "kt1", "123", "staff", "0911111111"),
            ("Kỹ thuật 2", "kt2", "123", "staff", "0922222222")
        ])

    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO customers (ten, sdt, dia_chi)
        VALUES (?, ?, ?)
        """, [
            ("Nguyễn Văn A", "0901234567", "Hà Nội"),
            ("Trần Văn B", "0912345678", "Hải Dương")
        ])

    conn.commit()
    conn.close()

    print("✅ DB READY")


if __name__ == "__main__":
    init_db()