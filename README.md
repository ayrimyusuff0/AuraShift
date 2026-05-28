# AuraShift: AI-Powered Unity Game

Python (MediaPipe) ile gerçek zamanlı el takibi yaparak Unity oyun motorunu kontrol eden yapay zeka projesi.

### 🎮 Oyunu İndir ve Oyna
Projenin oynanabilir tam sürümünü (.exe ve motorlar dahil) aşağıdan indirebilirsiniz: 👉 [AuraShift Tam Sürüm İndir (Google Drive)](https://drive.google.com/file/d/1VMm_4QKiLyc87bstDoCSU1IyNSQYvoom/view?usp=sharing)

---
📄 PROJE GELİŞTİRME VE TEKNİK RAPOR

Proje Adı: AuraShift
Proje Amacı: Python (MediaPipe) ile yapay zeka tabanlı el takibi yaparak, Unity oyun motorunu eşzamanlı olarak kontrol etmek.

1. Karşılaşılan Teknik Sorunlar

Derleme Hatası: Python kaynak kodu PyInstaller ile .exe formatına dönüştürülürken, MediaPipe kütüphanesinin alt modülleri (solutions) pakete eksik dahil olmuş ve çalışma zamanı hatalarına yol açmıştır.

Sürüm Uyumsuzluğu: Sistemdeki en güncel Python sürümü (3.13) ile görüntü işleme kütüphaneleri arasında ortam (environment) çakışmaları yaşanmıştır.

2. Geliştirilen Çözüm Mimarisi

Ortam İzolasyonu: Hatalı güncel sürüm yerine, kütüphanelerin en stabil çalıştığı tespit edilen Python 3.11.14 (Conda) ortamı doğrudan projeye entegre edilmiştir.

Eşzamanlı Başlatıcı (Batch Script): .exe derleme sorununu aşmak ve her iki motoru (Python ve Unity) gecikmesiz, aynı anda çalıştırabilmek için asenkron bir Windows .bat scripti yazılmıştır.

3. Sonuç ve Sunum Kararı

Entegrasyon %100 stabil hale getirilmiştir.

Proje sunumu için, Python arka planında çalışan kamera ve analiz ekranı özellikle açık bırakılmıştır. Bu sayede, yapay zekanın oyuncunun el hareketlerini (iskelet/landmark noktalarını) nasıl okuduğunun anlık bir "Teknoloji Demosu" olarak sergilenmesi hedeflenmiştir.
