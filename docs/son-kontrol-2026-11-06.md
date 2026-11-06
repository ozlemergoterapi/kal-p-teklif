# LS MoldWorks — son kontrol, 6 Kasım 2026

## Karar

Kontrollü ilk teklif denemesi yapılabilir. Kurumsal satışa ve denetimsiz otomatik kalıp/fiyat üretimine hazır olduğu söylenemez. 7 Kasım denemesinin hedefi, STEP + müşteri talebi → göz alternatifleri → incelenmiş taslak ve manuel düzeltme → maliyet ve üç kâr oranı → onay → referans düzende PDF → kapat/aç ve yedek doğrulamasıdır. Otomatik taslağın mühendislik doğruluğu ayrıca kontrol edilmelidir.

## Bu incelemede bulunan ve düzeltilenler

| Bulgu | Etki | Düzeltme / doğrulama |
|---|---|---|
| Yeni teknik taslakların içindeki öğrenme ve referans nesneleri eski yedek şemasına uymuyordu | Gerçek analizli teklifin yedeklenmesi/klasöre kaydı reddedilebilirdi | Yeni alanlara tip/boyut doğrulaması eklendi; gerçek analizli teklifin arşiv özeti artık doğrulanıyor |
| Satış satırları ve toplam farklı aşamalarda yuvarlanıyordu | Müşteri PDF'sinde 1 sent toplam farkı olabiliyordu | Satış ve trim ayrı ayrı sente yuvarlanır, toplam bu değerlerden alınır; Excel iç maliyet hassasiyeti korunur |
| Yalnız malzeme girilmiş V4 teklifinde işçilik/hırdavat sessizce eksik kalabiliyordu | Eksik maliyetle onay riski | İlgili grup maliyeti yoksa gider eklenmesi veya gerçekten ek gider gerekmeme nedeninin yazılması gerekir; diğer eksik fiyat kontrolleri de devam eder |
| Başka sayfaya geçerken veya yenilerken DOM'daki son girdiler yakalanmıyordu | Son değişiklik kaybolabilirdi | Geçişten önce yakalama ve kayıt; hata varsa geçiş engellenir |
| Dosya analizi sırasında sayfadan çıkılırsa son analiz sonucu kalıcı olmayabiliyordu | Eklenen dosya ve indeks sonucu kaybolabilirdi | Dosya işlemi bittiğinde ilgili proje de kaydedilir, eski onay geçersiz kılınır |
| Yeni üç adımlı akışta arşiv PDF kısayolu gizli alana gidiyordu | PDF düğmesine ulaşmak zorlaşıyordu | Çıktı adımı açılır ve doğru alana yönlenir |
| Outlook MSG doğrudan okunmuyordu | Gönderilen gerçek e-postalar program içinde işlenemiyordu | MSG gövdesi/konusu okuma ve paket bağımlılığı eklendi; gerçek FTT25153 maili uç noktada HTTP 200 ile okundu. Ekteki modeller ayrıca yüklenir |
| Kayıt alanı dolduğunda yalnız hata gösteriliyordu | Kaydedilmeyen son girdileri kurtarmak zordu | Son girdileri içeren indirilebilir kurtarma JSON'u eklendi; gerçek indirme ve yedek doğrulaması test edildi |
| Çıktıya dahil edilmeyen alternatifler kişisel örnek havuzuna girebiliyordu | İstenmeyen ölçüler öneri kaynağı olabilirdi | Hariç alternatifler öğrenme havuzundan çıkarıldı |
| Teklif kodunun yılı işletim sistemi tarihinden alınıyordu | İstanbul yıl geçişinde yanlış yıl olabilirdi | Teklif tarihiyle aynı İstanbul takvim yılı kullanılır |
| Boş firma kâr oranı kaydedilirken sıfır sayılabiliyordu | İstenmeyen sıfır kâr profili | Profildeki oran alanları zorunlu yapıldı |
| Eski hesap sürümüyle verilmiş onay yeniden kullanılabilirdi | Güncel sent hesabı ile eski onaylı çıktı karışabilirdi | Onay parmak izine hesap sürümü eklendi; eski onaylar yeniden inceleme gerektirir, arşivde yeniden kontrol durumunda görünür |

## Test sonucu

- 63 JavaScript testi geçti; 37 JavaScript dosyası sözdizimi kontrolünden geçti.
- 14 Python testi geçti: CAD/IGES, doküman/OCR, geometri/ağ ve PDF.
- CAD, Unicode PDF, OCR ve MSG çalışma ortamı ön kontrolü geçti.
- Windows NSIS/Mac PKG yapılandırması doğrulandı. Bu, yükleyicilerin gerçek işletim sisteminde kurulup çalıştığı anlamına gelmez.
- Linux geliştirme Electron uygulaması kendi yerel servisiyle açıldı; uygulama hazır, klasör seçimi API'si mevcut, renderer'da Node erişimi kapalı. Paketlenmiş Mac/Windows testi değildir.
- Gerçek STEP ağıyla teknik ekran, referans ölçüler, manuel değişiklik ve kg güncelleme çalıştı.
- Gerçek teklif akışı Hazır → Onay bekliyor → Onaylandı durumlarından geçti; düğmeden gerçek PDF indirildi.
- Türkçe onaylı iki alternatif iki ayrı A4 sayfada; İngilizce taslak işareti, kapsam durumları ve fiyat satırları ayrıca doğrulandı.
- Gerçek teknik/öğrenme verisiyle yedek şeması, revizyonun eski kaydı koruması, sayfa geçişinde kayıt ve onayın bozulması, PDF kısayolu doğrulandı.
- PDF'deki döküm ve trim satırlarının toplamı ondalık aritmetik ile kontrol edildi; sent farkı yok.
- Depolama hatası simülasyonunda kurtarma dosyası son girilen talebi içerdi; normal kayıt yeniden çalıştı.

Test kanıtları çalışma alanında `/workspace/artifacts/son-kontrol/` altındadır. Müşteri dosyaları ve özel analiz arşivi Git deposuna eklenmemiştir.

## Çalışan ve korunacak bölümler

| Bölüm | Durum ve sınır |
|---|---|
| Üç adımlı teklif ekranı | Çalışıyor; ayrıntılar kapalı, fiyat özeti görünür, eksik alana yönlendirme var |
| Firma bazlı arşiv/kod/revizyon | Çalışıyor; tek kullanıcı kapsamı |
| V4 maliyet yöntemi | Grup bazlı üç oran, manuel değişiklik ve canlı fiyat; kayıtlı referans aritmetiği testli |
| Çelik kataloğu | 10 V4 çeliği ve fiyat; firma fiyatları korunur, hizmetler ayrı |
| STEP/katı IGES | Gerçek geometri okunuyor; hatalı ve yüzey-only veri reddedilebilir |
| PDF/görsel/DXF/EML/MSG | Talep ve ölçü adayları çıkarılır; metin, düzenli örüntü ve OCR yöntemi. Her teknik şartın anlamını kavrayan genel yapay zekâ değildir |
| Yalnız 2D ile teklif | Üç ölçü ve belge doğrulamasıyla blok ön hesabı; 2D'den kesin maça analizi yapılmaz |
| Maça ekle/sil/etkinleştir/ölçülendir | Çalışıyor; kg ve maliyet tekrar hesaplanıyor, son maça kaldırılınca kapsam temizleniyor |
| Referans boyutlandırma | Dört tam hamil/çekirdek eşleştirmesi ve beş benzersiz maça profili üzerinden başlangıç önerisi; bütün arşivden genellenmiş mühendislik modeli değildir |
| Onay ve fiyat değişikliği | Geçerli onaydan sonra çıktı; değişiklik onayı bozar, eksikler nihai onayı engeller |
| Referans teklif formu | Firma kimliği/logo, müşteri başlığı, teknik tablo, sağ görsel, döküm/trim ve koşullar; gerçek PDF, TR/EN, ayrı alternatif sayfaları |
| Klasör/ZIP/JSON | Kod doğrulaması ve dosya bütünlüğü kontrolleri var; JSON orijinal dosyaları içermez, ZIP/klasör içerir. Gerçek Mac/Windows klasör izinleri ayrıca denenmeli |

## Açık kalanlar — öncelik sırası

### 1. Büyük arşiv için ana depolama (yayın öncesi kritik)

Ana proje listesi hâlâ localStorage kullanıyor. İzole Chromium denemesinde 35.051 baytlık örnek kayıttan yaklaşık 149 ek kopyada kota doldu. Bu sabit teklif limiti değildir; logo, görsel, teklif uzunluğu ve mevcut kullanım sonucu değiştirir. Ortak klasöre kopyalamak bu ana kayıt kotasını kaldırmaz. Kurtarma yedeği eklendi, fakat ölçek sorunu çözülmedi. Kurumsal kullanım öncesi projeler ve dosyalar için kalıcı veritabanı/dosya deposu ve göç/geri yükleme testi gerekir. Disk/klasör arşivi ve JSON/ZIP yedeği ilk denemede birlikte kullanılmalı.

### 2. Son sürümün Mac ve Windows yükleyicileri (ilk bilgisayar denemesi için kritik)

Yerelde son değişiklikler var; GitHub'a gönderilmedi. Bu sürümü içeren PKG/EXE üretildiği veya gerçek Mac Apple Silicon/Windows bilgisayara kurulup açıldığı doğrulanmadı. İkon, kısayol, çevrimdışı ilk açılış, Türkçe OCR, klasör izni, PDF indirme ve kaldır/yükle sonrası veri korunması gerçek cihazda denenmeli. İmzalama/notarization durumu gerçek paket üzerinde kontrol edilmeli. Linux geliştirme açılışı bunun yerine geçmez.

### 3. Kesin otomatik kalıp/maça tasarımı (işlev sınırı)

Mevcut yöntem örneklenmiş görünürlük/ters açı adayı ve ham blok taslağıdır. Ayrım hattı, büzülme, soğutma, yolluk, itici, piston kuvveti, gerçek mekanizma zarfı ve tam çarpışma/dayanım doğrulanmaz. Kalınlık toplamlarını ikiye eşit bölme varsayımı ekranda belirtilir. Sonuç mühendis kontrolü olmadan imalat tasarımı veya kesin ölçü sayılmamalı. Arşivdeki bazı SolidWorks taslaklarının yalnız önizlemesi okunabildi; tüm yerleşimler sayısal olarak çözümlenmiş değildir.

### 4. İşçilik saatleri ve piston maliyetinin otomatik tahmini

V4'ün fiyat aritmetiği ile saat/ücret satırları çalışıyor. Yeni parçadan güvenilir CNC/erozyon/montaj saati, kalıp büyüklüğüne göre piston fiyatı ve tam hırdavat listesi otomatik türetilmiş değil. Malzeme analizi yapılınca bunların hazır olduğu sanılmamalı. Yeni eksik gider kontrolü bu riski azaltır; otomatik tahminin kendisini sağlamaz.

### 5. Parasolid, CATIA ve SolidWorks yerel okuma

Canlı yetenek yanıtı yalnız STEP/IGES doğal CAD desteği ve `licensedTranslator: false` gösteriyor. Parasolid/CATIA için lisanslı çevirici bağlanmadı. SolidWorks SLDPRT/SLDASM yerel geometri okuma uygulamada yok. Formatların orijinalini saklamak, geometrisini okumak değildir. İlk deneme için önceki dosyalardan okunabilen STEP örnekleri kullanılabilir; kullanıcıdan arşivi yeniden göndermesi gerekmiyor.

### 6. Öğrenmenin kapsamı

Her uygulanan teknik taslak kendi teklifinde örnek saklar; yalnız geçerli onaylı ve çıktı kapsamındaki örnekler yeni önerilere katılır. Aynı model/düzen revizyonları çoğaltılmaz. Benzer göz, eksen, düzen, maçalı yapı ve ölçekte en yakın beş örnekten pay/kalınlık medyanı alınır. Bu yerel referans uyarlamasıdır; genel yapay zekâ eğitimi değildir. Saat/piston fiyatı öğrenmez; maça ekleyip çıkarma kararını otomatik devralmaz; kodunu değiştirmez. Tahmin hatası ölçümü ve yeterli bağımsız örnekle kalibrasyon hâlâ gerekir.

### 7. Doküman, OCR ve benzerlik sınırları

Türkçe/İngilizce talep örüntüleri var; OCR şu anda İngilizce dil modeliyle çalışıyor. Karmaşık teknik resimlerin her ölçüsünü, notunu ve kapsamını güvenilir şekilde otomatik okuyacağı garanti edilmez. MSG ekleri otomatik model olarak açılmaz. Teknik kapsam boşsa “Belirtilmedi” görünür; müşteriye göndermeden tamamlanmalı. Aynı parçayı bulma, dosya hash'i ve hacim/alan/atalet adaylarıdır; farklı geometriler benzer özellikler taşıyabilir. Aynı parça onayı kullanıcıda kalır.

### 8. Ölçek ve hata senaryoları

Çok büyük CAD dosyaları (yükleme sınırı 50 MB), 100 bin üçgen/3 bin yüz, yüzlerce teklif, büyük logolar ve ağ klasörü kesintileri için geniş performans/uzun süre testi yapılmadı. Sunucu/veritabanı göçü sonrası bu senaryolarla tekrar test gerekir. Çökme sonrası otomatik sürümlü tam yedek ve bağımsız makinede tam geri yükleme ayrıca denenmeli.

## Kapsam dışı olanlar eksik sayılmıyor

Çoklu kullanıcı ve rol/yetki sistemi kullanıcı talimatıyla şimdilik kapsam dışı. Bu inceleme yeni rol veya onaycı gerektirmiyor. Tek kullanıcı iç onay akışı korunuyor.

## 7 Kasım denemesi için önerilen sıra

1. Son sürümün verilerini koruyan depolama düzeni ve yedek stratejisi kesinleştirilir; üretim için localStorage sınırı kaldırılır.
2. Aynı sürümden Mac Apple Silicon/Windows kurulumları alınır ve gerçek bilgisayarda çevrimdışı açılış/PDF/kayıt test edilir.
3. Daha önce gönderilmiş, modeli ve hesabı doğrulanmış bir parça referans alınır; çekirdek/hamil/maça ölçüsü, kg, V4 tutarı ve saat satırları elle hesapla karşılaştırılır.
4. Aynı dosyadan 2 ve 4 gözlü alternatif, maça ekle/çıkar, manuel ölçü ve üç kâr oranı denenir.
5. Onay → gerçek PDF → klasör/ZIP → kapat/aç → geri yükleme yapılır; hem TR hem EN müşteri çıktısı kontrol edilir.
6. Ancak bu sonuçlardan sonra kontrollü gerçek teklif kullanımına geçilir. Yeni özellik eklemek yerine bu açıkları kapatmaya odaklanılır.
