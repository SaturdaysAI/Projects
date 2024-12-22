import streamlit as st
import time
import sqlite3


def setup_database():
    """Initialize database connection and create necessary tables."""
    for attempt in range(5):
        try:
            conn = sqlite3.connect('integrated_system.db', timeout=30, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL')
            c = conn.cursor()

            # Create users table
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (username TEXT PRIMARY KEY, 
                          password TEXT,
                          email TEXT,
                          profile_pic BLOB,
                          created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

            # Create comprehensive parking analytics table
            c.execute('''CREATE TABLE IF NOT EXISTS parking_analytics
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                          empty_spots INTEGER,
                          filled_spots INTEGER,
                          efficiency REAL,
                          revenue REAL,
                          peak_hour TEXT,
                          image_path TEXT,
                          notes TEXT)''')

            # Create video analytics table
            c.execute('''CREATE TABLE IF NOT EXISTS video_analytics
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp DATETIME,
                          empty_spots INTEGER,
                          filled_spots INTEGER)''')

            # Create daily summary table for faster querying
            c.execute('''CREATE TABLE IF NOT EXISTS daily_summaries
                         (date DATE PRIMARY KEY,
                          avg_empty_spots REAL,
                          avg_filled_spots REAL,
                          avg_efficiency REAL,
                          total_revenue REAL,
                          peak_hours TEXT,
                          total_vehicles INTEGER)''')

            # Create document processing table
            c.execute('''CREATE TABLE IF NOT EXISTS document_processing
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          file_path TEXT,
                          processing_date DATETIME,
                          status TEXT,
                          error_message TEXT)''')

            conn.commit()
            return conn, c
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < 4:
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff
            else:
                raise

    raise Exception("Failed to setup database after multiple attempts")


def migrate_database(c, conn):
    """Perform necessary database migrations."""

    # Check if email column exists
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]

    if 'email' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")

    if 'profile_pic' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN profile_pic BLOB")

    # Check if columns exist in parking_analytics
    c.execute("PRAGMA table_info(parking_analytics)")
    columns = [column[1] for column in c.fetchall()]

    columns_to_add = {
        'efficiency': 'REAL',
        'revenue': 'REAL',
        'peak_hour': 'TEXT',
        'image_path': 'TEXT',
        'notes': 'TEXT'
    }

    for column, data_type in columns_to_add.items():
        if column not in columns:
            c.execute(f"ALTER TABLE parking_analytics ADD COLUMN {column} {data_type}")
            conn.commit()
            print(f"Added {column} column to parking_analytics table")

    # Ensure document_processing table exists
    c.execute('''CREATE TABLE IF NOT EXISTS document_processing
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  file_path TEXT,
                  processing_date DATETIME,
                  status TEXT,
                  error_message TEXT)''')

    # Check if video_analytics table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video_analytics'")
    if not c.fetchone():
        c.execute('''CREATE TABLE video_analytics
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp DATETIME,
                      empty_spots INTEGER,
                      filled_spots INTEGER)''')
        conn.commit()
        print("Created video_analytics table")
        
    conn.commit()
    print("Ensured document_processing table exists")

    return conn, c


def update_daily_summary(date):
    """Update or create daily summary for the given date."""
    c = st.session_state.cursor
    
    # Get daily statistics
    c.execute('''SELECT 
                   avg(empty_spots) as avg_empty,
                   avg(filled_spots) as avg_filled,
                   avg(efficiency) as avg_eff,
                   sum(revenue) as total_rev,
                   group_concat(distinct peak_hour) as peak_hrs,
                   sum(filled_spots) as total_vehicles
                 FROM parking_analytics 
                 WHERE date(timestamp) = ?''', (date,))
    
    stats = c.fetchone()
    if stats[0] is not None:  # If we have data for this date
        c.execute('''INSERT OR REPLACE INTO daily_summaries
                     (date, avg_empty_spots, avg_filled_spots, avg_efficiency,
                      total_revenue, peak_hours, total_vehicles)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (date, *stats))
        st.session_state.conn.commit()
