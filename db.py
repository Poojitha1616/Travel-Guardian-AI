"""SQLite database layer."""
import sqlite3, bcrypt, uuid
from datetime import datetime, timedelta

DB_PATH = "travelguardian.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn(); c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT DEFAULT 'USER',
      reset_token TEXT, reset_expires TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS wallets (user_id TEXT PRIMARY KEY, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS transactions (id TEXT PRIMARY KEY, user_id TEXT,
      amount REAL, type TEXT, description TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS bookings (id TEXT PRIMARY KEY, user_id TEXT, type TEXT,
      from_city TEXT, to_city TEXT, date TEXT, amount REAL, status TEXT DEFAULT 'CONFIRMED',
      refund REAL DEFAULT 0, created_at TEXT);
    """)
    conn.commit()
    for email, name, pw, role, bal in [
        ("admin@tg.ai", "Admin", "admin123", "ADMIN", 10000),
        ("user@tg.ai", "Demo User", "user123", "USER", 20000),
    ]:
        c.execute("SELECT id FROM users WHERE email=?", (email,))
        if not c.fetchone():
            uid = str(uuid.uuid4())
            h = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            c.execute("INSERT INTO users (id,name,email,password,role,created_at) VALUES (?,?,?,?,?,?)",
                      (uid, name, email, h, role, datetime.now().isoformat()))
            c.execute("INSERT INTO wallets (user_id,balance) VALUES (?,?)", (uid, bal))
            conn.commit()
    conn.close()

def signup(name, email, password):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    if c.fetchone(): conn.close(); return None, "Email already registered"
    uid = str(uuid.uuid4())
    h = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    c.execute("INSERT INTO users (id,name,email,password,role,created_at) VALUES (?,?,?,?,?,?)",
              (uid, name, email, h, "USER", datetime.now().isoformat()))
    c.execute("INSERT INTO wallets (user_id,balance) VALUES (?,?)", (uid, 0))
    conn.commit(); conn.close()
    return get_user_by_id(uid), None

def login(email, password):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone(); conn.close()
    if not row: return None, "Invalid credentials"
    if not bcrypt.checkpw(password.encode(), row["password"].encode()):
        return None, "Invalid credentials"
    return dict(row), None

def get_user_by_id(uid):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = c.fetchone(); conn.close()
    return dict(row) if row else None

def create_reset_token(email):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    row = c.fetchone()
    if not row: conn.close(); return None
    token = uuid.uuid4().hex
    c.execute("UPDATE users SET reset_token=?, reset_expires=? WHERE id=?",
              (token, (datetime.now()+timedelta(hours=1)).isoformat(), row["id"]))
    conn.commit(); conn.close(); return token

def reset_password(token, new_password):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,reset_expires FROM users WHERE reset_token=?", (token,))
    row = c.fetchone()
    if not row: conn.close(); return False, "Invalid token"
    if datetime.fromisoformat(row["reset_expires"]) < datetime.now():
        conn.close(); return False, "Token expired"
    h = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    c.execute("UPDATE users SET password=?, reset_token=NULL, reset_expires=NULL WHERE id=?",
              (h, row["id"]))
    conn.commit(); conn.close(); return True, "Password updated"

def get_wallet(user_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM wallets WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO wallets (user_id,balance) VALUES (?,0)", (user_id,))
        conn.commit()
        c.execute("SELECT * FROM wallets WHERE user_id=?", (user_id,))
        row = c.fetchone()
    conn.close()
    return dict(row) if row else {"user_id": user_id, "balance": 0}

def add_transaction(user_id, amount, txn_type, description):
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO transactions (id,user_id,amount,type,description,created_at) VALUES (?,?,?,?,?,?)",
              (str(uuid.uuid4()), user_id, amount, txn_type, description, datetime.now().isoformat()))
    conn.commit(); conn.close()

def credit(user_id, amount, description, txn_type="CREDIT"):
    conn = get_conn(); c = conn.cursor()
    c.execute("UPDATE wallets SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit(); conn.close()
    add_transaction(user_id, amount, txn_type, description)

def debit(user_id, amount, description):
    w = get_wallet(user_id)
    if w["balance"] < amount: return False, "Insufficient balance"
    conn = get_conn(); c = conn.cursor()
    c.execute("UPDATE wallets SET balance = balance - ? WHERE user_id=?", (amount, user_id))
    conn.commit(); conn.close()
    add_transaction(user_id, amount, "DEBIT", description)
    return True, "OK"

def get_transactions(user_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close(); return rows

def create_booking(user_id, btype, from_city, to_city, date, amount):
    ok, msg = debit(user_id, amount, f"{btype} booking {from_city} -> {to_city}")
    if not ok: return None, msg
    bid = str(uuid.uuid4())
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO bookings (id,user_id,type,from_city,to_city,date,amount,status,refund,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (bid, user_id, btype, from_city, to_city, date, amount, "CONFIRMED", 0, datetime.now().isoformat()))
    conn.commit(); conn.close()
    return get_booking(bid), None

def get_booking(bid):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE id=?", (bid,))
    row = c.fetchone(); conn.close()
    return dict(row) if row else None

def get_bookings(user_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close(); return rows

CANCEL_FEE = 500

def cancel_booking(user_id, booking_id):
    b = get_booking(booking_id)
    if not b or b["user_id"] != user_id: return None, "Booking not found"
    if b["status"] == "CANCELLED": return None, "Already cancelled"
    refund = max(0, b["amount"] - CANCEL_FEE)
    conn = get_conn(); c = conn.cursor()
    c.execute("UPDATE bookings SET status='CANCELLED', refund=? WHERE id=?", (refund, booking_id))
    conn.commit(); conn.close()
    credit(user_id, refund, f"Refund for booking {booking_id[:8]}", "REFUND")
    return {"refund": refund, "fee": CANCEL_FEE}, None

def admin_all_users():
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,name,email,role,created_at FROM users ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]; conn.close(); return rows

def admin_all_bookings():
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]; conn.close(); return rows

def admin_analytics():
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT COUNT(*) AS n FROM users"); u = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM bookings"); b = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM bookings WHERE status='CANCELLED'"); cn = c.fetchone()["n"]
    c.execute("SELECT COALESCE(SUM(balance),0) AS s FROM wallets"); w = c.fetchone()["s"]
    conn.close()
    return {"users": u, "bookings": b, "cancelled": cn, "wallet_total": w}
