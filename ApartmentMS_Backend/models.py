from database import db

class Kullanici(db.Model):
    __tablename__ = 'kullanicilar'
    kullanici_adi = db.Column(db.String(255), primary_key=True)
    sifre = db.Column(db.String(255), nullable=False)
    uye_id = db.Column(db.Integer, db.ForeignKey('uyeler.id'), nullable=False)
    yetki_id = db.Column(db.Integer, db.ForeignKey('yetkiler.id'), nullable=False)

class Duyuru(db.Model):
    __tablename__ = 'duyurular'
    id = db.Column(db.Integer, primary_key=True)
    tarih = db.Column(db.Date, nullable=False)
    duyuru = db.Column(db.Text, nullable=False)

class Gelir(db.Model):
    __tablename__ = 'gelir'
    id = db.Column(db.Integer, primary_key=True)
    tarih = db.Column(db.Date, nullable=False)
    gelirturu = db.Column(db.String(255), nullable=False)
    tutar = db.Column(db.Numeric, nullable=False)

class Gider(db.Model):
    __tablename__ = 'gider'
    id = db.Column(db.Integer, primary_key=True)
    tarih = db.Column(db.Date, nullable=False)
    giderturu = db.Column(db.String(255), nullable=False)
    tutar = db.Column(db.Numeric, nullable=False)

class Uye(db.Model):
    __tablename__ = 'uyeler'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(255), nullable=False)
    soyad = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)

class Daire(db.Model):
    __tablename__ = 'daire'
    id = db.Column(db.Integer, primary_key=True)
    blok_id = db.Column(db.Integer, db.ForeignKey('bloklar.id'), nullable=False)
    kat = db.Column(db.Integer, nullable=False)
    daire_numarasi = db.Column(db.String(10), nullable=False)
    uye_id = db.Column(db.Integer, db.ForeignKey('uyeler.id'), nullable=False)

class Yetki(db.Model):
    __tablename__ = 'yetkiler'
    id = db.Column(db.Integer, primary_key=True)
    yetki = db.Column(db.String(255), nullable=False)

class Blok(db.Model):
    __tablename__ = 'bloklar'
    id = db.Column(db.Integer, primary_key=True)
    blok = db.Column(db.String(10), nullable=False)
