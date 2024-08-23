from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# Veritabanı nesnesi
db = SQLAlchemy()

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı bilgileri
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Veritabanı bağlantısını döndüren fonksiyon
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

# Bağlantıyı kontrol eden fonksiyon
def check_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname="postgres"  # İlk bağlantıyı genel veritabanına yapıyoruz
        )
        conn.close()
        print("Bağlantı başarılı.")
        return True
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return False

# Veritabanının var olup olmadığını kontrol eden fonksiyon
def check_database_exists():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname="postgres"  # Genel veritabanına bağlanıyoruz
    )
    conn.autocommit = True  # Veritabanı oluşturmak için autocommit'i açıyoruz
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    
    if not exists:
        print(f"Veritabanı '{DB_NAME}' bulunamadı, oluşturuluyor...")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Veritabanı '{DB_NAME}' oluşturuldu.")
    else:
        print(f"Veritabanı '{DB_NAME}' mevcut.")
    
    cur.close()
    conn.close()

# Tabloların var olup olmadığını kontrol eden fonksiyon
def check_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Tabloların adları
    tables = ['gelir', 'gider', 'duyurular', 'bloklar', 'yetkiler', 'uyeler', 'daire', 'kullanicilar']

    for table in tables:
        cur.execute(sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)"), [table])
        exists = cur.fetchone()[0]

        if not exists:
            print(f"Tablo '{table}' bulunamadı, oluşturuluyor...")
            create_table(cur, table)
            conn.commit()  # Tablo oluşturulunca değişiklikleri kaydet
        else:
            print(f"Tablo '{table}' mevcut.")
    
    cur.close()
    conn.close()

# Tablo oluşturma fonksiyonu
def create_table(cur, table_name):
    try:
        if table_name == 'gelir':
            cur.execute("""
            CREATE TABLE gelir (
                id SERIAL PRIMARY KEY,
                gelirturu VARCHAR(255) NOT NULL,
                tutar NUMERIC NOT NULL,
                tarih DATE NOT NULL
            )
            """)
        elif table_name == 'gider':
            cur.execute("""
            CREATE TABLE gider (
                id SERIAL PRIMARY KEY,
                giderturu VARCHAR(255) NOT NULL,
                tutar NUMERIC NOT NULL,
                tarih DATE NOT NULL
            )
            """)
        elif table_name == 'duyurular':
            cur.execute("""
            CREATE TABLE duyurular (
                id SERIAL PRIMARY KEY,
                duyuru TEXT NOT NULL,
                tarih DATE NOT NULL
            )
            """)
        elif table_name == 'bloklar':
            cur.execute("""
            CREATE TABLE bloklar (
                id SERIAL PRIMARY KEY,
                blok VARCHAR(10) NOT NULL
            )
            """)
        elif table_name == 'yetkiler':
            cur.execute("""
            CREATE TABLE yetkiler (
                id SERIAL PRIMARY KEY,
                yetki VARCHAR(255) NOT NULL
            )
            """)
        elif table_name == 'uyeler':
            cur.execute("""
            CREATE TABLE uyeler (
                id SERIAL PRIMARY KEY,
                ad VARCHAR(255) NOT NULL,
                soyad VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                telefon VARCHAR(50) NOT NULL
            )
            """)
        elif table_name == 'daire':
            cur.execute("""
            CREATE TABLE daire (
                id SERIAL PRIMARY KEY,
                blok_id INTEGER REFERENCES bloklar(id),
                kat INTEGER NOT NULL,
                daire_numarasi VARCHAR(50) NOT NULL,
                uye_id INTEGER REFERENCES uyeler(id)
            )
            """)
        elif table_name == 'kullanicilar':
            cur.execute("""
            CREATE TABLE kullanicilar (
                kullanici_adi VARCHAR(255) PRIMARY KEY,
                sifre VARCHAR(255) NOT NULL,
                uye_id INTEGER REFERENCES uyeler(id),
                yetki_id INTEGER REFERENCES yetkiler(id)
            )
            """)
        print(f"Tablo '{table_name}' oluşturuldu.")
    except Exception as e:
        print(f"Tablo '{table_name}' oluşturulurken hata: {e}")

def insert_data(): # Tablolara veri ekleme fonksiyonu
    conn = get_connection()
    cur = conn.cursor()

    try:
        # "yetkiler" tablosuna veri ekleme
        cur.execute("""
            INSERT INTO yetkiler (yetki) VALUES 
            ('Yönetici/Admin'), 
            ('Editör'), 
            ('Apartman Sakini')
        """)
        
        # "bloklar" tablosuna veri ekleme
        cur.execute("""
            INSERT INTO bloklar (blok) VALUES 
            ('A'), 
            ('B'), 
            ('C')
        """)
        
        # "uyeler" tablosuna veri ekleme
        cur.execute("""
            INSERT INTO uyeler (ad, soyad, email, telefon) VALUES 
            ('Admin_X_Name', 'Admin_X_Surname', 'adminxx@gmail.com', '0000000000')
        """)
        
        # "kullanicilar" tablosuna veri ekleme
        hashed_password = generate_password_hash('21')  # Şifreyi hash'leme
        cur.execute("""
            INSERT INTO kullanicilar (kullanici_adi, sifre, uye_id, yetki_id) VALUES 
            ('admin', %s, 1, 1)
        """, (hashed_password,))
        
        # Değişiklikleri kaydet
        conn.commit()
        print("Veriler başarıyla eklendi.")
        
    except Exception as e:
        print(f"Veri eklenirken hata oluştu: {e}")
        conn.rollback()  # Hata durumunda işlemi geri al
        
    finally:
        cur.close()
        conn.close()
