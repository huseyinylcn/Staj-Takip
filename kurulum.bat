@echo off
title Python Ortam Kurulumu
color 0A

echo ==========================================
echo 1. ADIM: Eski sanal ortam (venv) kontrol ediliyor...
echo ==========================================

if exist venv (
    echo Eski "venv" klasoru bulundu. Siliniyor...
    rmdir /s /q venv
    echo Silme islemi tamamlandi.
) else (
    echo Silinecek eski bir ortam bulunamadi, devam ediliyor.
)

echo.
echo ==========================================
echo 2. ADIM: Yeni sanal ortam olusturuluyor...
echo ==========================================
python -m venv venv

if %errorlevel% neq 0 (
    color 0C
    echo HATA: Python bulunamadi veya ortam olusturulamadi!
    echo Lutfen Python'un yuklu oldugundan ve PATH'e eklendiginden emin olun.
    pause
    exit
)

echo Sanal ortam olusturuldu.

echo.
echo ==========================================
echo 3. ADIM: Paketler requirements.txt'den yukleniyor...
echo ==========================================

if exist requirements.txt (
    .\venv\Scripts\pip install -r requirements.txt
) else (
    color 0C
    echo HATA: requirements.txt dosyasi bulunamadi!
)

echo.
echo ==========================================
echo ISLEM TAMAMLANDI!
echo ==========================================
pause