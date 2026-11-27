# Testler

`import_edevlet.py` için regresyon testleri. Testler gerçek bir e-Devlet belgesi kullanmaz. `edevlet_fixture.py`, uydurma "Örnek ailesi"nden (`assets/example/familytree.json`) bir "Alt-Üst Soy Bilgisi" PDF'i üretir.

PDF'in düzeni, tarayıcıda "Yazdır > PDF olarak kaydet" ile alınmış gerçek bir belgeden ölçüldü. Ölçülenler şunlar: sayfa boyutu, sütun konumları, satır aralığı, çok satırlı hücrelerin nasıl bölündüğü, tarayıcının üst ve alt bilgisinin yeri. Gerçek belgeden hiçbir ad, tarih, yer ya da numara alınmadı.

İki PDF üretilir:

- **temiz**: yalnızca tablo
- **yazdırılmış**: her sayfada tarayıcının üst bilgisi (tarih-saat, sayfa başlığı) ve alt bilgisi (adres, sayfa numarası). Adres, ikinci sayfanın ilk satırına gerçek belgedeki kadar yakındır. Eskiden bu adres o satırdaki adın önüne yapışıyor, sayfa numarası ("2 / 2") da aynı satırın "Durumu" hücresine düşüp yaşayan birini ölü gösteriyordu.

## Çalıştırma

Depo kökünden:

```
uv run --python 3.12 --with pypdf --with reportlab python -I tests/test_import_edevlet.py
```

Başka bir içe aktarıcıyı denemek için yolunu `IMPORTER` ile verin. Örneğin `main` dalındaki sürümü denemek için:

```
git show main:skills/family-migration-story/scripts/import_edevlet.py > /tmp/import_edevlet_main.py
IMPORTER=/tmp/import_edevlet_main.py uv run --python 3.12 --with pypdf --with reportlab python -I tests/test_import_edevlet.py
```

Testler pytest ile de çalışır (`--with pytest` ekleyip `python -I -m pytest tests`). Bir test başarısız olursa betik bütün farkları yazar ve 1 ile çıkar.

## Yazı tipi

Tabloda Türkçe harfler (İ, ı, ş, ğ) var. PDF'in hazır yazı tiplerinde bu harfler yok, bu yüzden bir TTF gerekir. Sırayla şunlara bakılır:

1. `EDEVLET_TEST_FONT` ortam değişkeni
2. DejaVu Sans (Linux)
3. Arial (macOS ve Windows)

Hiçbiri bulunamazsa testler atlanır ve nedeni yazılır. İçe aktarıcı harf genişliğini karakter sayısından tahmin eder, bu yüzden hangi yazı tipinin seçildiği sonucu değiştirmez.
