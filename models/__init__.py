from database import db
from datetime import datetime

class Sinif(db.Model):
    """Sınıf modeli"""
    __tablename__ = 'siniflar'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False, unique=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    ogrenciler = db.relationship('Ogrenci', backref='sinif', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S') if self.olusturma_tarihi else None
        }

class Ogrenci(db.Model):
    """Öğrenci modeli"""
    __tablename__ = 'ogrenciler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    ogrenci_no = db.Column(db.String(50), unique=True, nullable=False)
    telefon = db.Column(db.String(20))
    sinif_id = db.Column(db.Integer, db.ForeignKey('siniflar.id'), nullable=True)
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    ziyaret_notlari = db.relationship('ZiyaretNotu', backref='ogrenci', lazy=True, cascade='all, delete-orphan')
    staj_degerlendirme = db.relationship('StajDegerlendirme', backref='ogrenci', uselist=False, cascade='all, delete-orphan')
    normal_donem_degerlendirme = db.relationship('NormalDonemDegerlendirme', backref='ogrenci', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'ogrenci_no': self.ogrenci_no,
            'telefon': self.telefon,
            'sinif_id': self.sinif_id,
            'sinif_adi': self.sinif.ad if self.sinif else None,
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

class NormalDonemDegerlendirme(db.Model):
    """Normal dönem notu değerlendirme modeli"""
    __tablename__ = 'normal_donem_degerlendirme'
    
    id = db.Column(db.Integer, primary_key=True)
    ogrenci_id = db.Column(db.Integer, db.ForeignKey('ogrenciler.id'), nullable=False, unique=True)
    
    # Vize notları
    vize_notu = db.Column(db.Float, default=0)
    vize_odev_puani = db.Column(db.Float, default=None)  # Opsiyonel
    vize_odev_yuzdesi = db.Column(db.Float, default=0)  # Ödev puanının vizeye etki yüzdesi
    
    # Final notları
    final_notu = db.Column(db.Float, default=0)
    final_odev_puani = db.Column(db.Float, default=None)  # Opsiyonel
    final_odev_yuzdesi = db.Column(db.Float, default=0)  # Ödev puanının finale etki yüzdesi
    
    # Devamsızlık
    devamsizlik_durumu = db.Column(db.Boolean, default=False)  # False = kaldı, True = geçti
    
    # Bütünleme notları
    butunleme_notu = db.Column(db.Float, default=None)  # Opsiyonel
    butunleme_odev_puani = db.Column(db.Float, default=None)  # Opsiyonel
    butunleme_odev_yuzdesi = db.Column(db.Float, default=0)  # Ödev puanının büte etki yüzdesi
    
    # Otomatik hesaplanan
    vize_toplam = db.Column(db.Float, default=0)  # Vize + ödev (varsa)
    final_toplam = db.Column(db.Float, default=0)  # Final + ödev (varsa)
    butunleme_toplam = db.Column(db.Float, default=None)  # Büt + ödev (varsa)
    genel_toplam = db.Column(db.Float, default=0)  # Genel başarı notu
    harf_notu = db.Column(db.String(5))
    
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def hesapla_vize_toplam(self):
        """Vize toplamını hesapla (vize + ödev varsa)"""
        vize = self.vize_notu or 0
        
        if self.vize_odev_puani is not None and self.vize_odev_yuzdesi > 0:
            # Ödev puanı varsa, vize notunun (100 - yüzde) kadarını al, ödev puanının yüzde kadarını ekle
            vize_agirlik = (100 - self.vize_odev_yuzdesi) / 100
            odev_agirlik = self.vize_odev_yuzdesi / 100
            self.vize_toplam = (vize * vize_agirlik) + (self.vize_odev_puani * odev_agirlik)
        else:
            self.vize_toplam = vize
        
        return self.vize_toplam
    
    def hesapla_final_toplam(self):
        """Final toplamını hesapla (final + ödev varsa)"""
        final = self.final_notu or 0
        
        if self.final_odev_puani is not None and self.final_odev_yuzdesi > 0:
            # Ödev puanı varsa, final notunun (100 - yüzde) kadarını al, ödev puanının yüzde kadarını ekle
            final_agirlik = (100 - self.final_odev_yuzdesi) / 100
            odev_agirlik = self.final_odev_yuzdesi / 100
            self.final_toplam = (final * final_agirlik) + (self.final_odev_puani * odev_agirlik)
        else:
            self.final_toplam = final
        
        return self.final_toplam
    
    def hesapla_butunleme_toplam(self):
        """Bütünleme toplamını hesapla (büt + ödev varsa)"""
        if self.butunleme_notu is None:
            self.butunleme_toplam = None
            return None
        
        butunleme = self.butunleme_notu or 0
        
        if self.butunleme_odev_puani is not None and self.butunleme_odev_yuzdesi > 0:
            # Ödev puanı varsa, büt notunun (100 - yüzde) kadarını al, ödev puanının yüzde kadarını ekle
            but_agirlik = (100 - self.butunleme_odev_yuzdesi) / 100
            odev_agirlik = self.butunleme_odev_yuzdesi / 100
            self.butunleme_toplam = (butunleme * but_agirlik) + (self.butunleme_odev_puani * odev_agirlik)
        else:
            self.butunleme_toplam = butunleme
        
        return self.butunleme_toplam
    
    def hesapla_genel_toplam(self):
        """Genel başarı notunu hesapla"""
        # Devamsızlıktan kaldıysa genel toplam 0
        if not self.devamsizlik_durumu:
            self.genel_toplam = 0
            self.harf_notu = "FF"
            return self.genel_toplam
        
        # Bütünleme notu varsa onu kullan, yoksa normal vize+final
        if self.butunleme_toplam is not None:
            self.genel_toplam = self.butunleme_toplam
        else:
            # Vize %40, Final %60 (standart üniversite sistemi)
            vize_agirlik = 0.4
            final_agirlik = 0.6
            self.genel_toplam = (self.vize_toplam * vize_agirlik) + (self.final_toplam * final_agirlik)
        
        self.harf_notu = self.hesapla_harf_notu()
        return self.genel_toplam
    
    def hesapla_harf_notu(self):
        """Harf notunu hesapla - Resimdeki ölçek"""
        if not self.devamsizlik_durumu:
            return "FF"
        
        toplam = self.genel_toplam
        
        if toplam >= 82:
            return "AA"
        elif toplam >= 74:
            return "BA"
        elif toplam >= 65:
            return "BB"
        elif toplam >= 58:
            return "CB"
        elif toplam >= 50:
            return "CC"
        elif toplam >= 40:
            return "DC"
        elif toplam >= 35:
            return "DD"
        elif toplam >= 25:
            return "FD"
        else:
            return "FF"
    
    def hesapla_tum_notlar(self):
        """Tüm notları hesapla"""
        self.hesapla_vize_toplam()
        self.hesapla_final_toplam()
        self.hesapla_butunleme_toplam()
        self.hesapla_genel_toplam()
        return self.genel_toplam
    
    def to_dict(self):
        return {
            'id': self.id,
            'ogrenci_id': self.ogrenci_id,
            'vize_notu': self.vize_notu,
            'vize_odev_puani': self.vize_odev_puani,
            'vize_odev_yuzdesi': self.vize_odev_yuzdesi,
            'final_notu': self.final_notu,
            'final_odev_puani': self.final_odev_puani,
            'final_odev_yuzdesi': self.final_odev_yuzdesi,
            'devamsizlik_durumu': self.devamsizlik_durumu,
            'butunleme_notu': self.butunleme_notu,
            'butunleme_odev_puani': self.butunleme_odev_puani,
            'butunleme_odev_yuzdesi': self.butunleme_odev_yuzdesi,
            'vize_toplam': self.vize_toplam,
            'final_toplam': self.final_toplam,
            'butunleme_toplam': self.butunleme_toplam,
            'genel_toplam': self.genel_toplam,
            'harf_notu': self.harf_notu,
            'guncelleme_tarihi': self.guncelleme_tarihi.strftime('%Y-%m-%d %H:%M:%S') if self.guncelleme_tarihi else None
        }

