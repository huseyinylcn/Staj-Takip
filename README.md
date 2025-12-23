# 🎓 Staj Takip Sistemi

Öğretmenlerin öğrencilerin staj süreçlerini takip edebileceği, ziyaret notları düşebileceği ve staj değerlendirmesi yapabileceği **profesyonel ve kullanımı kolay** bir web uygulaması.

## ✨ Özellikler

### 👥 Öğrenci Yönetimi
- ✅ Öğrenci kayıt ve düzenleme
- ✅ Öğrenci arama ve filtreleme
- ✅ Excel ile toplu öğrenci ekleme
- ✅ Detaylı öğrenci profilleri

### 📝 Ziyaret Takibi
- ✅ Ziyaret notları ekleme/silme
- ✅ Tarih ve öğretmen adı kaydı
- ✅ Kronolojik not gösterimi
- ✅ Sınırsız not ekleme

### 📊 Staj Değerlendirme
- ✅ 8 farklı değerlendirme kriteri
- ✅ Otomatik toplam puan hesaplama
- ✅ Otomatik harf notu belirleme
- ✅ AA'dan FF'ye tam not sistemi

### 📁 Excel Entegrasyonu
- ✅ Öğrenci listesi Excel'e aktarma
- ✅ Excel'den öğrenci içe aktarma
- ✅ Detaylı değerlendirme raporu oluşturma
- ✅ Renkli ve formatlı Excel çıktıları

### 💾 Veritabanı
- ✅ SQLite (kurulum gerektirmez)
- ✅ Otomatik veritabanı oluşturma
- ✅ İlişkisel veri yapısı
- ✅ Güvenli veri saklama

### 🎨 Modern Arayüz
- ✅ Responsive tasarım (mobil uyumlu)
- ✅ Gradient renkler ve animasyonlar
- ✅ Font Awesome ikonlar
- ✅ Kullanıcı dostu formlar

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum (Önerilen)

**Windows:**
```cmd
kurulum.bat
```

**Linux/Mac:**
```bash
chmod +x kurulum.sh
./kurulum.sh
```

> Kurulum scripti:
> - ✅ Eski sanal ortamı siler (varsa)
> - ✅ Yeni sanal ortam oluşturur
> - ✅ Tüm paketleri yükler
> - ✅ Her şeyi otomatik yapar!

### Çalıştırma

**Windows:**
```cmd
calistir.bat
```

**Linux/Mac:**
```bash
chmod +x calistir.sh
./calistir.sh
```

### Manuel Kurulum (İsterseniz)

1. **Sanal ortam oluşturun:**
   ```bash
   python -m venv venv
   ```

2. **Sanal ortamı aktifleştirin:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Paketleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Uygulamayı başlatın:**
   ```bash
   python app.py
   ```

5. **Tarayıcıda açın:**
   ```
   http://localhost:5000
   ```

> 💡 **Not:** Otomatik kurulum her şeyi sizin için halleder!

## 📖 Detaylı Dökümanlar

- 📘 **[Hızlı Başlangıç](HIZLI_BASLANGIC.md)** - 5 dakikada başlayın!
- 📗 **[Kullanım Kılavuzu](KULLANIM_KILAVUZU.md)** - Tüm özellikler detaylı anlatım
- 📙 **[Mimari Dokümantasyon](MIMARI.md)** - Teknik detaylar ve mimari

## 🎯 Gereksinimler

- **Python:** 3.8 veya üzeri
- **İşletim Sistemi:** Windows, Linux, macOS
- **Tarayıcı:** Chrome, Firefox, Safari, Edge (modern sürümler)
- **Disk Alanı:** ~50 MB

## 🎬 Demo Verileri

Test için örnek veriler oluşturun:

```bash
# Windows
venv\Scripts\activate
python demo_verileri_olustur.py

# Linux/Mac
source venv/bin/activate
python3 demo_verileri_olustur.py
```

Bu şunları oluşturur:
- 8 örnek öğrenci
- 15+ ziyaret notu  
- 4 tamamlanmış değerlendirme

## 📸 Ekran Görüntüleri

### Ana Sayfa
- Öğrenci listesi ve istatistikler
- Hızlı arama ve filtreleme
- Toplu işlemler (Excel)

### Öğrenci Detay
- Öğrenci bilgileri
- Ziyaret notları listesi
- Staj değerlendirme formu

### Değerlendirme Sistemi
- 8 kriter puanlaması:
  - İşyeren Notu (30 puan)
  - İçindekiler (10 puan)
  - Firma Bilgisi (10 puan)
  - Yazım Düzeni (10 puan)
  - Resim & Şekil (10 puan)
  - Dil Kullanımı (20 puan)
  - Sonuç Bölümü (10 puan)
  - Defter Düzeni & Mülakat (30 puan)
- Otomatik toplam ve harf notu hesaplama

## 🏗️ Proje Yapısı

```
staj_takip/
├── 📄 app.py                    # Ana uygulama
├── 📄 database.py               # Veritabanı konfigürasyonu
├── 📁 models/                   # Veri modelleri
├── 📁 services/                 # İş mantığı
├── 📁 routes/                   # API endpoint'leri
├── 📁 templates/                # HTML sayfaları
├── 📁 static/                   # CSS & JavaScript
│   ├── css/
│   └── js/
├── 📄 requirements.txt          # Python bağımlılıkları
└── 📄 staj_takip.db            # SQLite veritabanı
```

## 🛠️ Teknolojiler

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy 3.1.1** - ORM
- **openpyxl 3.1.2** - Excel işlemleri
- **pandas 2.1.4** - Veri işleme

### Frontend
- **HTML5 & CSS3** - Modern arayüz
- **Vanilla JavaScript** - Dinamik içerik
- **Font Awesome 6.4.0** - İkonlar

### Database
- **SQLite 3** - Dosya bazlı veritabanı

## 💡 Özellik Detayları

### Öğrenci Yönetimi
```python
# Öğrenci ekleme
POST /api/ogrenciler
{
  "ad": "Ahmet",
  "soyad": "Yılmaz",
  "ogrenci_no": "20210101",
  "telefon": "05551234567"
}
```

### Ziyaret Notları
```python
# Ziyaret notu ekleme
POST /api/ziyaretler
{
  "ogrenci_id": 1,
  "ogretmen_adi": "Dr. Ahmet YILMAZ",
  "not_metni": "Staj yerine ziyaret yapıldı..."
}
```

### Değerlendirme
```python
# Staj değerlendirme
POST /api/degerlendirme/1
{
  "isyeren_notu": 28.0,
  "icindekiler": 9.0,
  "firma_bilgisi": 9.5,
  ...
}
```

## 📊 Veritabanı Şeması

### Ogrenci
- `id` (Primary Key)
- `ad`, `soyad`, `ogrenci_no` (Unique)
- `telefon`, `kayit_tarihi`

### ZiyaretNotu
- `id` (Primary Key)
- `ogrenci_id` (Foreign Key)
- `tarih`, `not_metni`, `ogretmen_adi`

### StajDegerlendirme
- `id` (Primary Key)
- `ogrenci_id` (Foreign Key, Unique)
- 8 değerlendirme kriteri
- `toplam` (hesaplanan), `harf_notu`

## 🔒 Güvenlik

- SQL Injection koruması (ORM kullanımı)
- XSS koruması (Template escape)
- Dosya yükleme validasyonu
- Input sanitization

## 🚨 Sorun Giderme

### Uygulama Başlamıyor
```bash
# Python versiyonunu kontrol edin
python --version  # 3.8+ olmalı

# Paketleri yeniden yükleyin
pip install -r requirements.txt
```

### Port Kullanımda Hatası
```python
# app.py'de portu değiştirin
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Veritabanı Hatası
```bash
# Veritabanını sıfırlayın
del staj_takip.db  # Windows
rm staj_takip.db   # Linux/Mac
```

## 📈 Performans

- **Öğrenci Kapasitesi:** ~10,000 öğrenci
- **Eşzamanlı Kullanıcı:** 1-5 kişi
- **Yanıt Süresi:** < 100ms (yerel)

Daha büyük sistemler için PostgreSQL önerilir.

## 🔄 Güncellemeler

### Versiyon 1.0.0 (2024)
- ✅ İlk stabil sürüm
- ✅ Tüm temel özellikler
- ✅ Excel import/export
- ✅ Kapsamlı dokümantasyon

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull request açın

## 📝 Lisans

MIT License - Özgürce kullanabilirsiniz!

## 📞 İletişim & Destek

Sorun yaşarsanız:
1. `KULLANIM_KILAVUZU.md` dosyasını inceleyin
2. `MIMARI.md` dosyasında teknik detayları bulun
3. Issue açın (GitHub)

## 🎓 Eğitim Amaçlı Kullanım

Bu proje eğitim kurumlarında kullanılmak üzere tasarlanmıştır:
- Üniversiteler
- Meslek yüksekokulları
- Teknik kolejler
- Meslek liseleri

## ⭐ Öne Çıkan Özellikler

### Kolay Kurulum
- Tek tıkla kurulum (`.bat` ve `.sh` dosyaları)
- Bağımlılık yönetimi otomatik
- Veritabanı otomatik oluşturulur

### Kullanıcı Dostu
- Sezgisel arayüz
- Türkçe dil desteği
- Hızlı arama ve filtreleme

### Güvenilir
- Otomatik hesaplamalar
- Veri tutarlılığı
- Hata yönetimi

### Genişletilebilir
- Temiz mimari
- Modüler yapı
- Kolay özelleştirme

## 🎯 Gelecek Planları

- [ ] PDF rapor oluşturma
- [ ] E-posta bildirimleri
- [ ] Çoklu kullanıcı desteği
- [ ] Grafik ve istatistikler
- [ ] Mobil uygulama

---

**Geliştirici:** AI + İnsan İşbirliği  
**Tarih:** 2024  
**Versiyon:** 1.0.0

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

