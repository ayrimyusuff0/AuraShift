@echo off
:: Python'u "pythonw.exe" ile başlatıyoruz (Siyah CMD ekranı çıkmaz, tamamen gizli çalışır)
start "" "C:\Users\yusuf\miniconda3\envs\aurashift\pythonw.exe" "oyun.py"

:: Unity oyununu başlatıyoruz ve .bat dosyasının oyunu BEKLEMESİNİ sağlıyoruz (başında start yok)
"AuraShift.exe"

:: Oyuncu Unity'den (oyundan) çıktığı an, aşağıdaki kod devreye girer ve arkadaki gizli Python'u kapatır
taskkill /F /IM pythonw.exe >nul 2>&1