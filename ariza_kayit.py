#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arıza Kayıt Programı - terminalden arıza kaydı ekleme, listeleme, güncelleme ve arama."""

import csv
import os
from datetime import datetime

# Kayıt dosyası programla aynı klasörde tutulur
DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ariza_kayitlari.csv")
ALANLAR = ["id", "tarih", "cihaz", "konum", "aciklama", "durum"]
DURUMLAR = ["Açık", "Çözüldü"]


def kayitlari_oku():
    """CSV dosyasındaki kayıtları okur; dosya yoksa boş liste döner."""
    if not os.path.exists(DOSYA):
        return []
    kayitlar = []
    try:
        with open(DOSYA, newline="", encoding="utf-8") as f:
            for satir in csv.DictReader(f):
                # Bozuk satırları atla (ID sayı değilse)
                if not satir.get("id", "").isdigit():
                    continue
                satir["id"] = int(satir["id"])
                kayitlar.append(satir)
    except (OSError, csv.Error) as hata:
        print(f"Uyarı: kayıt dosyası okunamadı ({hata}). Boş liste ile başlanıyor.")
    return kayitlar


def kayitlari_yaz(kayitlar):
    """Tüm kayıtları CSV dosyasına yazar."""
    try:
        with open(DOSYA, "w", newline="", encoding="utf-8") as f:
            yazici = csv.DictWriter(f, fieldnames=ALANLAR)
            yazici.writeheader()
            yazici.writerows(kayitlar)
    except OSError as hata:
        print(f"Hata: kayıtlar kaydedilemedi ({hata}).")


def bos_olmayan_girdi(mesaj):
    """Boş bırakılamayan metin girdisi alır."""
    while True:
        deger = input(mesaj).strip()
        if deger:
            # Virgül CSV'yi bozmaz ama satır sonu bozabilir; tek satıra indir
            return " ".join(deger.split())
        print("Bu alan boş bırakılamaz, tekrar deneyin.")


def sayi_girdisi(mesaj):
    """Pozitif tam sayı girdisi alır."""
    while True:
        deger = input(mesaj).strip()
        if deger.isdigit() and int(deger) > 0:
            return int(deger)
        print("Lütfen geçerli bir pozitif sayı girin.")


def ariza_ekle(kayitlar):
    """Yeni arıza kaydı oluşturur."""
    print("\n--- Yeni Arıza ---")
    yeni_id = max((k["id"] for k in kayitlar), default=0) + 1
    kayit = {
        "id": yeni_id,
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),  # tarih otomatik
        "cihaz": bos_olmayan_girdi("Cihaz: "),
        "konum": bos_olmayan_girdi("Konum: "),
        "aciklama": bos_olmayan_girdi("Arıza açıklaması: "),
        "durum": "Açık",  # yeni kayıt her zaman açık başlar
    }
    kayitlar.append(kayit)
    kayitlari_yaz(kayitlar)
    print(f"Arıza #{yeni_id} kaydedildi.")


def tablo_yazdir(kayitlar):
    """Kayıtları hizalı bir tablo olarak yazdırır."""
    if not kayitlar:
        print("Kayıt bulunamadı.")
        return
    print(f"\n{'ID':<4} {'Tarih':<17} {'Cihaz':<18} {'Konum':<18} {'Durum':<8} Açıklama")
    print("-" * 90)
    for k in kayitlar:
        print(f"{k['id']:<4} {k['tarih']:<17} {k['cihaz'][:18]:<18} {k['konum'][:18]:<18} {k['durum']:<8} {k['aciklama']}")
    print(f"Toplam: {len(kayitlar)} kayıt")


def durum_guncelle(kayitlar):
    """Seçilen kaydın durumunu Açık/Çözüldü olarak değiştirir."""
    if not kayitlar:
        print("Güncellenecek kayıt yok.")
        return
    kayit_id = sayi_girdisi("Güncellenecek arıza ID: ")
    kayit = next((k for k in kayitlar if k["id"] == kayit_id), None)
    if kayit is None:
        print(f"#{kayit_id} numaralı kayıt bulunamadı.")
        return
    print(f"Mevcut durum: {kayit['durum']}")
    secim = input("Yeni durum (1 = Açık, 2 = Çözüldü): ").strip()
    if secim not in ("1", "2"):
        print("Geçersiz seçim, durum değiştirilmedi.")
        return
    kayit["durum"] = DURUMLAR[int(secim) - 1]
    kayitlari_yaz(kayitlar)
    print(f"Arıza #{kayit_id} durumu '{kayit['durum']}' olarak güncellendi.")


def ara(kayitlar):
    """Cihaz veya konumda geçen kelimeye göre arama yapar (büyük/küçük harf duyarsız)."""
    terim = bos_olmayan_girdi("Aranacak kelime (cihaz/konum): ").casefold()
    sonuc = [k for k in kayitlar if terim in k["cihaz"].casefold() or terim in k["konum"].casefold()]
    tablo_yazdir(sonuc)


def main():
    kayitlar = kayitlari_oku()  # program açılınca kayıtlar yüklenir
    print(f"Arıza Kayıt Programı - {len(kayitlar)} kayıt yüklendi.")
    while True:
        print("\n1) Arıza ekle\n2) Arızaları listele\n3) Durum güncelle (Açık/Çözüldü)\n4) Ara (cihaz/konum)\n5) Çıkış")
        secim = input("Seçiminiz: ").strip()
        if secim == "1":
            ariza_ekle(kayitlar)
        elif secim == "2":
            tablo_yazdir(kayitlar)
        elif secim == "3":
            durum_guncelle(kayitlar)
        elif secim == "4":
            ara(kayitlar)
        elif secim == "5":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim, 1-5 arası bir sayı girin.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D ile düzgün çıkış
        print("\nÇıkılıyor...")
