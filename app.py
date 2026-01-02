from flask import Flask
from database import db, init_db
from routes.main_routes import main_bp
from models import Ogrenci, ZiyaretNotu, StajDegerlendirme, NormalDonemDegerlendirme, Sinif  # Modelleri import et ki tablolar oluşturulsun
import os

def create_app():
    """Flask uygulaması oluştur"""
    app = Flask(__name__)
    
    # Konfigürasyon
    app.config['SECRET_KEY'] = 'staj-takip-sistemi-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staj_takip.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Veritabanını başlat
    init_db(app)
    
    # Blueprint'leri kaydet
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🎓 STAJ TAKİP SİSTEMİ")
    print("=" * 60)
    print("✅ Sunucu başlatılıyor...")
    print("📍 Adres: http://localhost:5000")
    print("🛑 Durdurmak için: CTRL+C")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

