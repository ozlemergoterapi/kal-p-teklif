# Windows ve Mac masaüstü kurulumu

## Kullanıcı deneyimi

Windows 10/11 x64 için normal kurulum sihirbazı (`.exe`) hazırlanır. Kurulum klasörü seçilebilir; masaüstü ve Başlat menüsü kısayolu otomatik oluşturulur. Kurulum sonunda uygulama açılabilir. Python, Node, CAD paketleri, PDF araçları ve OCR bilgisayarda ayrıca kurulmaz; paket içinde gelir. İlk açılıştaki yerleştirme işlemi uygulamanın kendi ilerleme penceresinde gerçekleşir. Çalışma sırasında bu bileşenler internetten indirilmez.

Mac için Intel ve Apple Silicon ayrı `.pkg` dosyaları hazırlanır (macOS 13+). macOS yükleme sihirbazı uygulamayı `/Applications/LS MoldWorks.app` konumuna kurar. Kurulum sonrası betik, oturum açmış kullanıcının masaüstüne uygulamanın simgeli bağlantısını ekler. Mac çalışma ortamı bu sabit konuma göre paketlenir; uygulamayı başka klasöre taşımak desteklenmez. macOS'un masaüstü erişim izni gibi sistem izinleri engellenmişse kısayol eklenmesi de engellenebilir ve kurulum hata bildirir. Başka bir kullanıcı adına yapılan, oturumsuz otomatik kurulumda kısayol garanti edilmez.

Teklifler Electron kullanıcı veri klasöründe saklanır; eski tarayıcı çalışma kopyaları otomatik taşınmaz. Mevcut JSON/ZIP yedeği içe aktarılabilir. Firma sunucusu klasörü Ayarlar'dan ayrıca seçilir. Windows kaldırma işlemi kayıtları otomatik silmez. Uygulama sabit bir yerel adres kullanır; sürüm güncellemesi tarayıcı kaydının kökenini değiştirmez.

Parasolid/CATIA için ticari okuyucu bu depoda bulunmadığından bu kurulum onu sağlayamaz. STEP/IGES ve mevcut yerel belge analizi bileşenleri paketlenir; ticari CAD çeviricisi lisansı/dağıtım hakkı ayrıca sağlanmalıdır.

## Tek konumdan üç dosya

`.github/workflows/desktop-installers.yml` Windows x64, Mac Intel ve Mac Apple Silicon için kendi işletim sisteminde derleme yapar. Manuel `workflow_dispatch` veya main dalında uygulama/kurulum kodu değişiklikleri derlemeyi tetikler; otomatik GitHub Release oluşturma yoktur. Üçü başarıyla tamamlandığında aynı Actions çalışmasının `LS-MoldWorks-Windows-ve-Mac` indirme çıktısında toplanır. Başarısız bir platform varsa birleştirilmiş paket üretilmez.

Kod main dalına gönderildiğinde workflow tetiklenir; indirme dosyaları ancak native derlemeler başarıyla bittiğinde oluşur. Yerel Linux ortamındaki masaüstü açılış testi native Windows/Mac kurulum testi yerine geçmez. `.exe`/`.pkg` dosyalarının hazır olduğu iddia edilmemelidir.

## Derleme yapısı

- Electron ve electron-builder sürümleri package-lock ile sabitlenir.
- Native conda ortamına Python 3.12, Tesseract 5.5 ve requirements-cad.txt bağımlılıkları kurulur. Kullanıcının makinesinde conda kurulmaz.
- `scripts/pack-runtime.py` tüm ortamı `build/runtime` içine taşır. Windows'ta ilk açılışta kullanıcı veri klasörüne kopyalanıp conda-pack ile taşınabilir yollar düzeltilir. Mac'te sabit uygulama yoluna derleme sırasında yerleştirilir; bu sayede imzalanmış Mac içeriği açılışta değiştirilmez.
- Başlatma sırasında interpreter, CAD katısı oluşturma, PDF modülleri ve OCR dil verisi denetlenir. İnternet bağlantısı veya paket yöneticisi kullanılmaz.
- `npm run desktop:check` electron-builder şemasını ve varlık dosyalarını kontrol eder. `npm run check` masaüstü JavaScript dosyalarını da denetler. `npm test` taşıma, mimari kontrolü ve kısayol yapılandırmasını test eder.
- `npm run desktop:dev` geliştirici açılışıdır; son kullanıcı için değildir. Native derleme ortamında `npm run desktop:runtime`, ardından `npm run desktop:dist -- --x64` veya `--arm64` kullanılır. CLI `--publish never` ile yayın engellenir.

## İmzalama ve normal dağıtım

Sertifikasız dosyalar `-test` adıyla üretilir ve işletim sistemi güven uyarılarına yol açabilir. Bunlar doğrulanmış imzalı dağıtım olarak sunulmamalıdır.

GitHub Actions secret alanları:

- Windows: `WINDOWS_CSC_LINK`, `WINDOWS_CSC_KEY_PASSWORD` (uygun Windows kod imzalama sertifikası).
- Mac: `MAC_CSC_LINK`, `MAC_CSC_KEY_PASSWORD`; paket içeriğinin Developer ID Application sertifikası ve `.pkg` için Developer ID Installer sertifikası/özel anahtarı erişilebilir olmalıdır. Sertifika paketi iki kimliği içerebilir. `MAC_INSTALLER_IDENTITY` paket imzalama kimliğini seçer.
- Apple doğrulaması: `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`. mac.notarize uygulama notarization adımını etkinleştirir. Ardından `scripts/notarize-installer.mjs` son `.pkg` dosyasını Apple notarytool ile gönderir, sonucu bekler ve stapler ile bileti ekleyip doğrular. Son Gatekeeper davranışı ayrıca temiz Mac kabul testinde doğrulanmalıdır.

Sertifika verisi depoya yazılmaz. Signed modda kod imzası yoksa derleme başarısız olmalıdır. Sertifikalar ve dağıtım hesapları sağlanmadan uyarısız kurulum veya tamamlanmış notarization sözü verilemez.

## Dağıtım öncesi native kabul testi

Her hedefte Python/Node/Tesseract bulunmayan temiz bir bilgisayarda ağı kapatıp yükleyin. Kurulum sihirbazı, masaüstü simgesi, ilk ve ikinci açılış, STEP/IGES, taranmış PDF OCR, ölçü PDF indirme, şirket klasörüne kayıt, ZIP geri yükleme, kaldırıp yeniden yükleme ve kayıtların korunması test edilmelidir. Mac'te PKG signature/notarization/Gatekeeper; Windows'ta Authenticode ve kurulumun arka planda terminal açmaması doğrulanmalıdır. Şu an yerelde yapılandırma ve Linux Electron açılışı doğrulanmıştır; bu native kabul testleri henüz yapılmamıştır.
