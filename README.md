# Arıza Kayıt Programı

Cihaz arızalarını terminalden kaydetmek ve takip etmek için basit bir Python programı. Sadece standart kütüphane kullanır, ek kurulum gerektirmez.

## Özellikler

- Arıza ekleme (ID ve tarih otomatik)
- Tüm arızaları tablo halinde listeleme
- Durum güncelleme: **Açık** / **Çözüldü**
- Cihaz veya konuma göre arama
- Kayıtlar `ariza_kayitlari.csv` dosyasında tutulur, program açılınca otomatik okunur

## Çalıştırma

Python 3.8 veya üstü gerekir.

```bash
python ariza_kayit.py
```

Menüden 1–5 arası bir seçim yapın. Kayıt dosyası programla aynı klasörde oluşturulur.
