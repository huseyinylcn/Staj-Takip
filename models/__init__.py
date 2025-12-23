from database import db
from datetime import datetime

class Ogrenci(db.Model):
    """Öğrenci modeli"""
    __tablename__ = 'ogrenciler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    ogrenci_no = db.Column(db.String(50), unique=True, nullable=False)
    telefon = db.Column(db.String(20))
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    ziyaret_notlari = db.relationship('ZiyaretNotu', backref='ogrenci', lazy=True, cascade='all, delete-orphan')
    staj_degerlendirme = db.relationship('StajDegerlendirme', backref='ogrenci', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'ogrenci_no': self.ogrenci_no,
            'telefon': self.telefon,
            'kayit_tarihi': self.kayit_tarihi.strftime('%Y-%m-%d %H:%M:%S') if self.kayit_tarihi else None,
            'tam_ad': f"{self.ad} {self.soyad}"
        }

class ZiyaretNotu(db.Model):
    """Öğretmen ziyaret notları modeli"""
    __tablename__ = 'ziyaret_notlari'
    
    id = db.Column(db.Integer, primary_key=True)
    ogrenci_id = db.Column(db.Integer, db.ForeignKey('ogrenciler.id'), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    not_metni = db.Column(db.Text, nullable=False)
    ogretmen_adi = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'ogrenci_id': self.ogrenci_id,
            'tarih': self.tarih.strftime('%Y-%m-%d %H:%M:%S') if self.tarih else None,
            'not_metni': self.not_metni,
            'ogretmen_adi': self.ogretmen_adi
        }

class StajDegerlendirme(db.Model):
    """Staj dosyası değerlendirme notu modeli"""
    __tablename__ = 'staj_degerlendirme'
    
    id = db.Column(db.Integer, primary_key=True)
    ogrenci_id = db.Column(db.Integer, db.ForeignKey('ogrenciler.id'), nullable=False, unique=True)
    
    # Değerlendirme kriterleri (Resimden alınan bilgiler)
    ziyaretci_ogretim_elemani_notu = db.Column(db.Float, default=0)  # 0%
    isyeren_notu = db.Column(db.Float, default=0)  # 30% - 10 puan
    icindekiler = db.Column(db.Float, default=0)  # 10 puan
    firma_bilgisi = db.Column(db.Float, default=0)  # 10 puan
    yazim_duzeni = db.Column(db.Float, default=0)  # 10 puan
    resim_sekil = db.Column(db.Float, default=0)  # 10 puan
    dil_kullanimi = db.Column(db.Float, default=0)  # 20 puan
    sonuc_bolumu = db.Column(db.Float, default=0)  # 10 puan
    defter_duzeni_mulakat = db.Column(db.Float, default=0)  # 30 puan
    
    # Otomatik hesaplanan
    toplam = db.Column(db.Float, default=0)
    harf_notu = db.Column(db.String(5))
    
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def hesapla_toplam(self):
        """Toplam puanı hesapla"""
        self.toplam = (
            self.isyeren_notu +
            self.icindekiler +
            self.firma_bilgisi +
            self.yazim_duzeni +
            self.resim_sekil +
            self.dil_kullanimi +
            self.sonuc_bolumu +
            self.defter_duzeni_mulakat
        )
        self.harf_notu = self.hesapla_harf_notu()
        return self.toplam
    
    def hesapla_harf_notu(self):
        """Harf notunu hesapla - Yeni ölçek"""
        if self.toplam >= 82:
            return "AA"
        elif self.toplam >= 74:
            return "BA"
        elif self.toplam >= 65:
            return "BB"
        elif self.toplam >= 58:
            return "CB"
        elif self.toplam >= 50:
            return "CC"
        elif self.toplam >= 40:
            return "DC"
        elif self.toplam >= 35:
            return "DD"
        elif self.toplam >= 25:
            return "FD"
        else:
            return "FF"
    
    def to_dict(self):
        return {
            'id': self.id,
            'ogrenci_id': self.ogrenci_id,
            'ziyaretci_ogretim_elemani_notu': self.ziyaretci_ogretim_elemani_notu,
            'isyeren_notu': self.isyeren_notu,
            'icindekiler': self.icindekiler,
            'firma_bilgisi': self.firma_bilgisi,
            'yazim_duzeni': self.yazim_duzeni,
            'resim_sekil': self.resim_sekil,
            'dil_kullanimi': self.dil_kullanimi,
            'sonuc_bolumu': self.sonuc_bolumu,
            'defter_duzeni_mulakat': self.defter_duzeni_mulakat,
            'toplam': self.toplam,
            'harf_notu': self.harf_notu,
            'guncelleme_tarihi': self.guncelleme_tarihi.strftime('%Y-%m-%d %H:%M:%S') if self.guncelleme_tarihi else None
        }

