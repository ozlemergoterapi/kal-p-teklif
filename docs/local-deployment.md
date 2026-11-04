# Tek kullanıcı ile yerel / firma içi kullanım

Uygulama Node.js sunucusu ve Python/OpenCascade analiz süreciyle firmanın kendi bilgisayarında çalışabilir. Harici CAD servisine bağlantı gerekmez. Kurulumdaki paket indirme erişimiyle çalışma sırasındaki yerel analiz ayrı konulardır. Bu sürümde çoklu kullanıcı, oturum veya yetki yönetimi yoktur.

## Ön koşullar ve başlatma

Node.js 22+ ve Python 3.12 önerilir. Mevcut Linux ortamında çalıştırıldı; diğer işletim sistemlerinde bağımlılık tekerleklerinin (wheels) uygunluğu ayrıca doğrulanmalıdır.

Depo kökünde:

```sh
python3 -m venv .venv-cad
.venv-cad/bin/python -m pip install -r requirements-cad.txt
npm ci --no-audit --no-fund
npm run check
npm test
npm run start:local
```

Windows'ta venv için `python -m venv .venv-cad`, paket kurulumu için `.venv-cad\Scripts\python.exe -m pip install -r requirements-cad.txt` kullanılır. Başlatıcı bu sanal ortamı otomatik bulur. Alternatif Python `LS_CAD_PYTHON` ile seçilebilir. Varsayılan port 3000, yerel adres 127.0.0.1'dir. Port `PORT` ile değişir.

Bir firma içi sunucudan sunmak için `HOST` bilinçli olarak değiştirilir. Tarayıcı klasör seçimi, localhost dışında güvenilir HTTPS gerektirir; kurumun HTTPS ters vekili kullanılmalıdır. Uygulamayı internete açık, kimlik doğrulaması olmayan bir servis olarak sunmak bu tek kullanıcı sürümünün kapsamı değildir.

## Kayıt konumunu elle seçme

1. Firma ve Fiyat Ayarları → Kayıt Konumu → Kayıt klasörü seç.
2. Yerel bir klasör veya işletim sisteminde bağlı ve yazılabilir ağ paylaşımını seçin. Sunucunun dosya yolu tarayıcıya yazılarak erişim sağlanamaz; klasör kullanıcının bilgisayarından erişilebilir olmalıdır.
3. Mevcut arşivi klasöre kaydet ile kayıtlı verileri aktarın. Sonraki kayıtlar aynı hedefe yazılır. Tarayıcıda da bir çalışma kopyası tutulur.
4. Uygulama yeniden açıldığında gerekirse Klasör iznini yenile kullanın. İzin veya ağ hatası ekranda belirtilir; klasöre yazıldı iddiasında bulunulmaz.

Seçilen klasörde:

```text
LS-MoldWorks/
  workspace.json
  firmalar/
    KP-<müşteri-kimliği>/
      KP26001.json
      KP26001_rev1.json
      KP26001.paket/
        teklif.json
        talep.txt
        dosya-listesi.json
        teklif.approved.html
        ekler/
          <SHA256>--model.step
          <SHA256>--çizim.pdf
```

`workspace.json` tüm kaydedilmiş teklifleri, müşteri kartlarını, firma ayarlarını ve logoyu içerir. Firma altındaki JSON dosyaları tek proje kayıtlarıdır. Klasördeki arşivi aç, önce birleştirme ön izlemesi sunar; mevcut kayıtlar sessizce ezilmez. Hedef değişikliği eski klasördeki dosyaları kaldırmaz. Orijinal STEP/PDF ekleri ve tarayıcıdan yazdırılan PDF dosyaları otomatik olarak bu klasöre kaydedilmez. Bunlar ayrı tutulmalıdır.

Klasör yazımı bir sunucu veri tabanı değildir. Bu sürümde aynı arşivi eş zamanlı birden fazla cihazın yazması desteklenmez. Manifest en son yazılır; kesinti olursa başarısızlık bildirilir ve tarayıcıdaki çalışma kopyası korunur. Ayrı dosyalara yazım tüm klasörü kapsayan atomik bir işlem değildir.

## Onay ve maliyet

Hazırlanıyor → Hazır → Onay bekliyor → İncele ve onayla. Eksik bilgiler durum geçişini engeller. Onay kutusu ayrıca işaretlenir; içerik/fiyat değişikliği onayı geçersiz kılar. Bu, teklif hazırlayan kişinin iç kontrolüdür ve müşteri sipariş onayı değildir. Seçilen klasöre son onay kaydı yazılamazsa onay tamamlanmaz.

İç maliyet dökümü çekirdek blok bedeli, ayrı maliyet satırları, miktar/saat, birim fiyat ve kâr hesabını gösterir. Hamil/maça/piston/hırdavat satırları elle veya katalogdan eklenir. Tam otomatik kalıp boyutlandırması değildir. Her alternatifte manuel satış veya maliyet üzerine kâr seçilebilir; trim ayrı açılır/kapanır ve oranı değiştirilebilir. İç maliyetler müşteri çıktısında gösterilmez.

Onay sonrası aynı firma klasöründe `KP26001.approved.html` de oluşturulur; görsel/logo ve stiller dosyaya gömülüdür. Bu dosya tarayıcıda açılıp yazdırılabilir. Onaylı içerik değiştirilip kaydedildiğinde artık geçersiz olan onaylı HTML kaldırılır; yeniden onayla yenisi oluşturulur. Klasör veya çıktı kaydı başarısız olursa onay bekleme durumuna döner. Kaydedilmiş teklif çalışma kopyasının tarayıcı kotası bu sürümde hâlâ geçerlidir.


## Tam paket ve geri yükleme

Projedeki Teklif dosya paketini indir düğmesi, orijinaller dahil bir ZIP oluşturur. Yedekleme ekranında bu ZIP seçilirse dosyalar CRC ve SHA-256 ile kontrol edilir; teklifler inceleme adımından sonra birleştirilir. Yalnızca uygulamanın kendi sıkıştırmasız ZIP biçimi desteklenir. JSON yedeği orijinal binary dosyaları içermez. Klasördeki arşivi aç ise metadata ve paket klasöründeki dosyaları beraber bağlar. Erişilemeyen orijinaller açıkça bildirilir ve teklif son onayı için tamamlanmaları gerekir.

Güncel fiyatlarla hesaplama, onaylı kaydı değiştirmek yerine yeni revizyon ve ayrı alternatif oluşturur. Eski alternatif yeni çıktıda kapsam dışı kalır; eski revizyon kendi onayı ve dosyalarıyla korunur.


## 3D teknik ekran

`npm ci` sonrasındaki postinstall adımı Three.js ve OrbitControls dosyalarını `public/vendor` altında hazırlar. Üretim/yerel kurulumda bu adım atlanmamalıdır. STEP üçgenleme uç noktası POST /api/mesh'tir; aynı CAD Python ortamını kullanır. Geometri ve üçgenleme aynı anda tek iş çalıştırır. WebGL 2 destekli güncel tarayıcı gerekir. Yerel görüntüleme ağda üçüncü taraf CAD servisi kullanmaz.

## Belge okuma ve özel CAD çeviricileri

`requirements-cad.txt` PyMuPDF, Pillow ve ezdxf içerir. Ayrıca işletim sisteminde Tesseract OCR komutu ve `eng` dil verisi kurulmalıdır (Debian/Ubuntu: `tesseract-ocr`, `tesseract-ocr-eng`). Belge metni/OCR yerel çalışır, harici yapay zeka servisine gönderilmez. Kurallar ve sınırlar [document-analysis.md](document-analysis.md) dosyasındadır. Parasolid/CATIA için lisanslı çevirici hazır değildir; yapılandırılmadan bu biçimlerin analizi çalışmaz.
