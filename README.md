# LS MoldWorks

## Mac’te çift tıklayarak çalıştırma

Node 22, Python 3.12 ve Tesseract zaten kuruluysa:

1. GitHub’dan **Code → Download ZIP** ile güncel programı indirin ve ZIP’i açın.
2. Program klasörünün içindeki **LS-MoldWorks-Baslat.command** dosyasına çift tıklayın.
3. İlk açılışta gerekli Python ve Electron paketleri otomatik indirilir; işlem tamamlanınca uygulama açılır. Terminal penceresini işlem sürerken kapatmayın. Komut yazmanız gerekmez.

Tek başına başlatıcıyı indirecekseniz **LS-MoldWorks-Mac-Baslat.zip** dosyasını indirin ve açın. Başlatıcı program klasörünün dışında kalırsa klasörü seçmenizi ister. Bu, tam bağımsız PKG kurulumunun yerine geçen bir yükleyici değil, mevcut geliştirici kurulumunu otomatik hazırlayan başlatıcıdır. Mac güvenlik engeli gösterirse Sistem Ayarları → Gizlilik ve Güvenlik bölümünden dosyaya izin vermeniz gerekebilir.


Yüksek basınçlı alüminyum enjeksiyon kalıpları için tek kullanıcılı teklif uygulaması prototipi. Türkçe arayüz, Türkçe/İngilizce teklif çıktısı.

## Çalıştırma

Node.js 22+, CAD araması için Python/OpenCascade gerekir. Sunucu Node yerleşik modüllerini kullanır; tarayıcıdaki Three.js sürümü package-lock.json ile sabitlenmiştir. Npm kurulumu görüntüleyici dosyalarını yerel olarak hazırlar; uygulama çalışırken CDN gerekmez.

```sh
python3 -m venv .venv-cad
.venv-cad/bin/python -m pip install -r requirements-cad.txt
npm ci --no-audit --no-fund
npm run check
npm test
npm run start:local
```

Windows / firma içi sunucu ve kayıt klasörü kuralları: [docs/local-deployment.md](docs/local-deployment.md). Mevcut bir CAD Python ortamı `LS_CAD_PYTHON` ile seçilebilir. `npm start` da sunucuyu başlatır; varsayılan adres 127.0.0.1, port 3000'dir. Süreçler yeniden açılışta tekrar başlatılır. Mevcut checkout kullanılır, worktree gerekmez.

## Hazır özellikler

- Logolu açılış, ana ekran, müşteri kartları, firma/durum/metin ile arşiv arama.
- Müşteri/yıl kodları (KP26001), yeni kodla kopyalama, `_rev1` revizyonları.
- Hazırlanıyor → Hazır → Onay bekliyor → İncele ve onayla. Ayrı teklif onay kutusu; içerik değişince onay geçersizleşir.
- Firma unvanı/logo/iletişim, çelik/piston kataloğu, iki dilde ticari koşullar, firmaya özel hesap profili.
- Ham çekirdek blok ölçü/ağırlık/bedeli; bağımsız göz alternatifleri, maça/kızak kapsamı, ek maliyet satırları, maliyet üzerine kâr, isteğe bağlı trim hesabı.
- Manuel satış fiyatı veya hesaplanan fiyat seçimi. Her alternatif kendi toplamına sahiptir; alternatifler birbirine eklenmez. İç maliyetler müşteri çıktısına eklenmez.
- Tarayıcı kaydı veya elle seçilen yerel/bağlı ağ klasörüne kayıt. Klasör izni IndexedDB'de saklanır; yeniden izin gerekebilir.
- Firma klasörlerinde proje JSON dosyaları, tüm arşiv için workspace.json ve her teklif için .paket klasörü. Paket; orijinal belgeler, talep metni, dosya listesi ve onaylı yazdırılabilir HTML içerir. PDF yazdırma ekranından ayrıca kaydedilir.
- Sürümlü JSON yedekleme / geri yükleme, orijinaller dahil proje ZIP paketi indirme/geri yükleme ve çakışan kayıtları koruma. Yeni seçilen klasörde mevcut arşiv varsa önce inceleme/birleştirme gerekir.
- STEP için gerçek OpenCascade hacim, yüzey alanı, asal atalet imzası; yeniden adlandırılan/döndürülen modellerden eski teklif adayı arama. Aynı dosya için SHA-256 eşleştirme.
- Gerçek STEP 3D görüntüleme, döndürme/zoom, yüz seçimi, iki nokta ölçümü, kesit kırpma ve sağ/sol karşılaştırma.
- Düzenlenebilir göz yerleşimi, çekirdek/hamil/maça ham blokları; ağırlık ve çelik bedelini teklife aktarma.
- Benzerlik adayını referans bağlamadan önce zorunlu kullanıcı onayı; onay eski fiyatı değiştirmez.

## Hesap kuralları ve sınırlar

Temel kenar payı: 100 mm parça boyutuna kadar her kenarda 70 mm, üstünde her 10 mm için 5 mm artış (ara değerlerde doğrusal). Firma/proje ayarlarından değişir. Başlangıç göz arası 40 mm, iki ham blok ve %20 kâr deneme varsayımlarıdır. Trim başlangıç oranı döküm teklifinin yaklaşık üçte biridir. Kg fiyatı bilinmiyorsa boş kalır; sıfır fiyat uydurulmaz.

Çekirdek blok ağırlığı: mm³ × kg/m³ / 1e9 × adet. Hamil, piston, hırdavat ve işleme kalemleri manuel veya katalogdan eklenir. STEP üzerinden düzenlenebilir ham blok ön taslağı vardır; imalata hazır otomatik kalıp/maça/hamil tasarımı ve işleme süresi tahmini yoktur.

STEP analizinin geçici sunucu kopyası işlemden sonra silinir; orijinal dosya tarayıcı dosya deposunda ve seçilmişse arşiv klasöründe korunur (50 MB, 120 sn, tek analiz). Kapalı ve geçerli katılar kullanılır; yardımcı yüzey/eğriler ölçü imzasına katılmaz. Aynı katı sayısı ve en fazla %12 özellik sapması aday üretir; en fazla %2 çok yakın olarak etiketlenir. Bunlar geçici arama eşikleridir, güven yüzdesi değildir. Sağ/sol veya farklı parçalar aynı özellikleri taşıyabilir; kullanıcı onayı her zaman gerekir. Katı IGES STEP’e çevrilerek analiz edilir. PDF metni/OCR, görüntü, EML, TXT ve DXF metninden talep/ölçü adayları çıkarılır; kullanıcı onayıyla uygulanır. Parasolid/CATIA için lisanslı çevirici gerekir. Bkz. docs/document-analysis.md. Eski kayıtlar, STEP yeniden seçilip kaydedilerek indekslenir.

Kayıtlar tarayıcıda çalışma kopyası olarak kalır; tarayıcı kotası geçerlidir. Klasör seçimi Chromium/Edge ve güvenli bağlam gerektirir. Ortak sunucu klasörü önce işletim sisteminden erişilebilir olmalıdır. Yeni eklenen orijinal CAD/PDF ve müşteri belgeleri IndexedDB dosya deposunda tutulur; seçili klasöre kayıt sırasında teklif paketine kopyalanır. Eski metadata kayıtları için orijinaller yeniden seçilmelidir. Tarayıcıdan yeni oluşturulan PDF çıktısı ayrıca kaydedilir. Aynı arşive eş zamanlı çoklu cihaz yazımı, kullanıcı/yetki sistemi ve genel işlem geçmişi bu sürümde yoktur.

## Kontroller

`npm test` maliyet, onay, yedek, model adayları ve gerçek geçici klasör yazımı testlerini tek Node sürecinde çalıştırır. `npm run test:cad` OpenCascade ile döndürülmüş/yeniden kaydedilmiş geometri ve bozuk dosya kontrollerini çalıştırır. Tarayıcıda firma profili, maliyet/trim, onay durumları, onay değişmezliği, gerçek tarayıcı dosya sistemi yazımı/geri okuma, eski arşiv koruması ve bağlantı hatası senaryoları ayrıca doğrulandı. Klasör seçme diyaloğu testte otomatik sağlandı; dosya yazımı gerçek tarayıcı DirectoryHandle üzerinde yapıldı. Gerçek bir müşteri ağ sunucusuna bağlantı bu ortamda test edilmedi.

## Dosya paketi, tarihler ve güncel fiyatlar

- Orijinaller SHA-256 anahtarıyla IndexedDB'de saklanır; metadata localStorage'da kalır. Aynı adlı farklı dosyalar hash ile ayrılır. Dosyaya erişim ve onay öncesi orijinal varlığı kontrol edilir. Klasörden geri açmada içerik hash'leri doğrulanır.
- Proje ZIP paketi kayıt, talep metni, orijinaller, dosya listesi ve varsa güncel teklif çıktısını içerir. Yedekleme ekranı bu uygulamanın sıkıştırmasız ZIP paketini okuyup dosyaları doğrulayarak geri yükler; metadata değişiklikleri kullanıcı incelemesinden sonra uygulanır. Genel amaçlı/sıkıştırılmış ZIP içe aktarımı desteklenmez. ZIP limiti 250 MB, tek dosya limiti 50 MB'dir. JSON yedeği tek başına binary dosya içermez.
- Teklif tarihi ve isteğe bağlı müşteri dönüş tarihi proje içinde düzenlenir. Geçerlilik sonu teklif tarihi + geçerlilik günüdür; son günün sonunda dolar. Ana ekranda geciken dönüşler, önümüzdeki üç gün ve süresi dolmuş teklifler filtrelenir. Gün hesabı Europe/Istanbul takvimindedir.
- Güncel fiyat düğmesi eski hesap ve geometriyi değiştirmeden yeni alternatif önerir. Çelik adı, piston marka/modeli ve işçilik türüne göre güncel katalog/tarifeler kullanılır. Bilinmeyen veya elle değiştirilmiş fiyatlar tahmin edilmez; yeni hesapta tamamlanmak üzere boş bırakılır.
- Onaylı teklifte güncelleme yeni revizyon açar, eski onayı korur. Yeni revizyonda eski alternatif karşılaştırma amacıyla korunur, yeni müşteri çıktısına dahil edilmez; güncel alternatif ayrıca onaylanır. Ölçüler ve kenar kuralları fiyat yenilemesinde değiştirilmez.

## Teknik inceleme

Her alternatifte 3D incele ve kalıp taslağı oluştur düğmesi bulunur. Öneri mantığı, parametreler, ücret aktarımı ve sınırlar [docs/technical-review.md](docs/technical-review.md) içinde açıklanır. WebGL 2 gereklidir. Görüntüleme önbelleği IndexedDB dosya deposunun 2. sürümündedir; orijinaller korunarak yükseltilir. Eski sekmeler geçişi engellerse kapatılıp yeniden açılmalıdır.

## Windows / Mac kurulum paketleri

Terminal gerektirmeyen Electron masaüstü uygulaması ve Windows EXE / Mac PKG derleme yapısı eklendi. Python/CAD/PDF/OCR çalışma ortamı paketin içine alınır. GitHub Actions üç platformun dosyalarını aynı indirme çıktısında toplar. Native yükleyiciler bu oturumda henüz üretilmedi; imza ve temiz makine testleri ayrıca gerekir. [Kurulum ve derleme ayrıntıları](docs/desktop-installation.md).
