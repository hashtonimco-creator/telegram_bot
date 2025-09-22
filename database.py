import sqlite3
import datetime

def init_database():
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()

    # Create publishers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            phone_number TEXT,
            telegram_username TEXT,
            page_username TEXT,
            publisher_code TEXT UNIQUE,
            access_code TEXT UNIQUE,
            is_active BOOLEAN DEFAULT 1,
            registration_date TEXT,
            created_by_admin INTEGER
        )
    ''')
    
    # Add missing columns if they don't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE publishers ADD COLUMN publisher_code TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE publishers ADD COLUMN access_code TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE publishers ADD COLUMN created_by_admin INTEGER')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            added_by INTEGER,
            date_added TEXT NOT NULL
        )
    ''')

    # Create stores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_url TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_date TEXT NOT NULL
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER,
            discount INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_date TEXT NOT NULL,
            FOREIGN KEY (store_id) REFERENCES stores (id)
        )
    ''')

    # Insert default store
    cursor.execute('''
        INSERT OR IGNORE INTO stores (id, name, base_url, created_date)
        VALUES (1, 'کره بادام زمینی لایف استایل', 'lfshop.ir/life100', ?)
    ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

    # Insert default product
    cursor.execute('''
        INSERT OR IGNORE INTO products (id, store_id, name, description, price, discount, created_date)
        VALUES (1, 1, 'کره بادام زمینی ارگانیک', 'کره بادام زمینی 100% خالص، بدون شکر افزوده', 370000, 100000, ?)
    ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

    conn.commit()
    conn.close()

def add_publisher(user_id, phone_number, telegram_username):
    """Legacy function for direct publisher registration (without access code)"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate a simple publisher code for legacy registrations
    publisher_code = f"L{user_id}"  # L for Legacy
    access_code = f"LEGACY_{user_id}"
    
    try:
        cursor.execute('''
            INSERT INTO publishers (user_id, phone_number, telegram_username, publisher_code, access_code, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, phone_number, telegram_username, publisher_code, access_code, registration_date))
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists, maybe update info if needed
        pass
    finally:
        conn.close()

def get_publisher(user_id):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM publishers WHERE user_id = ?', (user_id,))
    publisher = cursor.fetchone()
    conn.close()
    return publisher

def get_publisher_by_id(publisher_id):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM publishers WHERE id = ?', (publisher_id,))
    publisher = cursor.fetchone()
    conn.close()
    return publisher

def update_page_username(user_id, page_username):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE publishers
        SET page_username = ?
        WHERE user_id = ?
    ''', (page_username, user_id))
    conn.commit()
    conn.close()

def get_all_publishers():
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, phone_number, telegram_username, page_username FROM publishers')
    publishers = cursor.fetchall()
    conn.close()
    return publishers

def add_admin(user_id, username, added_by):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
            INSERT INTO admins (user_id, username, added_by, date_added)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, added_by, date_added))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def is_admin(user_id):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    admin = cursor.fetchone()
    conn.close()
    return admin is not None

def get_all_admins():
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username FROM admins')
    admins = cursor.fetchall()
    conn.close()
    return admins

def remove_admin(user_id):
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
    conn.commit()
    deleted = conn.total_changes > 0
    conn.close()
    return deleted

# New functions for enhanced system

def create_publisher_by_admin(page_username, publisher_code, access_code, admin_id):
    """Create a publisher entry by admin without user_id (pre-setup)"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # If no publisher_code provided, generate next available P0X format
    if not publisher_code:
        cursor.execute('SELECT MAX(CAST(SUBSTR(publisher_code, 3) AS INTEGER)) FROM publishers WHERE publisher_code LIKE "P0%"')
        result = cursor.fetchone()
        next_num = (result[0] or 0) + 1
        publisher_code = f"P0{next_num}"
    
    try:
        cursor.execute('''
            INSERT INTO publishers (page_username, publisher_code, access_code, registration_date, created_by_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (page_username, publisher_code, access_code, registration_date, admin_id))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_publisher_by_access_code(access_code):
    """Get publisher by access code"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM publishers WHERE access_code = ?', (access_code,))
    publisher = cursor.fetchone()
    conn.close()
    return publisher

def activate_publisher_account(access_code, user_id, phone_number, telegram_username):
    """Activate publisher account when they join via access code"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE publishers 
        SET user_id = ?, phone_number = ?, telegram_username = ?, is_active = 1
        WHERE access_code = ?
    ''', (user_id, phone_number, telegram_username, access_code))
    conn.commit()
    updated = conn.total_changes > 0
    conn.close()
    return updated

def get_all_stores():
    """Get all active stores"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stores WHERE is_active = 1')
    stores = cursor.fetchall()
    conn.close()
    return stores

def get_products_by_store(store_id):
    """Get all active products for a store"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE store_id = ? AND is_active = 1', (store_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def add_store(name, base_url):
    """Add new store"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
            INSERT INTO stores (name, base_url, created_date)
            VALUES (?, ?, ?)
        ''', (name, base_url, created_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def add_product(store_id, name, description, price, discount=0):
    """Add new product to store"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
            INSERT INTO products (store_id, name, description, price, discount, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (store_id, name, description, price, discount, created_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_all_publishers_for_admin():
    """Get all publishers including pre-created ones"""
    conn = sqlite3.connect('hashtonim_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, page_username, publisher_code, access_code, 
               phone_number, telegram_username, is_active 
        FROM publishers ORDER BY id
    ''')
    publishers = cursor.fetchall()
    conn.close()
    return publishers

# Alias for backward compatibility
def init_db():
    return init_database()

# Initialize the database and tables when the module is first imported
init_database()
