@echo off
title Uygulama Baslatiliyor...
color 0B

echo ==========================================
echo Sanal ortam aktif ediliyor...
echo ==========================================

:: Sanal ortam klasorunun varligini kontrol et
if not exist venv (
    color 0C
    echo HATA: "venv" klasoru bulunamadi!
    echo Lutfen once kurulum.bat dosyasini calistirin.
    pause
    exit
)

:: Sanal ortamdaki python.exe'yi dogrudan cagirarak app.py'yi calistir
:: Bu yontem "activate" komutundan daha kararli ve hizlidir.
echo Uygulama (app.py) calistiriliyor...
echo ------------------------------------------

.\venv\Scripts\python.exe app.py

:: Program kapanirsa veya hata verirse hemen kapanmasin diye beklet
if %errorlevel% neq 0 (
    echo.
    echo ------------------------------------------
    echo Bir hata olustu veya program kapandi.
    pause
) else (
    echo.
    echo Program basariyla sonlandi.
    pause
)