# Teknik inceleme ve ham kalıp taslağı

## Kullanım

1. Projeye orijinal STEP dosyasını ekleyin; alternatifte 3D incele ve kalıp taslağı oluştur seçin.
2. Ana modeli seçin. Döndürme, zoom, kaydırma, standart görünümler, yüz seçimi ve iki yüzey noktası arası ölçüm kullanılabilir. Kesit, kırpma düzlemiyle görüntülemeyi açar; kapatılmış kesit yüzeyi veya ölçülendirilmiş imalat resmi üretmez. Ölçüm, üçgen ağ üzerinde yaklaşık nokta seçimine dayanır; BRep üzerinde hassas ölçüm değildir.
3. Gerçek sağ modeli ayrıca seçebilirsiniz. Yoksa sağ/sol görünüşü yalnız aynalanmış ön izlemedir. Aynalamanın gerçek sağ parça olduğu kabul edilmez. Maça adayları ana model üzerinden hesaplanır; sağ model ayrıca ana model seçilerek incelenmelidir.
4. Açılma ekseni X/Y/Z arasından seçilir. Satır/sütun, göz arası, kenar payı ve aynı parça/sağ-sol çiftleri düzenlenir. Göz sayısı yerleşimle eşleşmezse taslak uygulanamaz.
5. Gözler ve kalıp blokları görünümü ham malzemeleri gösterir. Çekirdek/hamil boyutları elle değiştirilebilir. Açılma ekseni değiştiğinde eski eksene bağlı manuel blok ölçüleri otomatiğe döner; maça koordinatları yeni U/V/açılma eksenlerine çevrilir.
6. Turuncu aday yüzlerden, seçili yüzden veya elle maça ham bloğu eklenir. Adet tekrarını kapatma, etkinlik, ölçü, konum ve yön düzenlenebilir. Aynı otomatik bölge ikinci kez eklenmez.
7. Çelik türü/yoğunluk/kg fiyatı girildiğinde ağırlık ve ham malzeme bedeli güncellenir. Bilinmeyen fiyat boş kalır. Görünüş teklif görseli olarak kaydedilebilir.
8. Ölçü ve malzemeleri teklife uygula, aktif alternatifin ölçülerini ve ham stok hesabını günceller. Önceden otomatik üretilmiş teknik maliyet satırlarını yeniler; diğer giderleri korur. Değişiklik onayı geçersiz kılar.

## Parametreler

- Temel kenar payı firma/alternatifteki mevcut kuraldan gelir: varsayılan 100 mm'ye kadar 70 mm, üzerindeki her 10 mm için 5 mm artış.
- Gözler arası 40 mm, çekirdek arka payı 40 mm, hamil duvarı 30 mm, taban 40 mm, maça çevresi 20 mm ve maça arka payı 30 mm deneme varsayımlarıdır. Doğrulanmış tasarım standartları değildir; arayüzde değiştirilebilirler.
- İki çekirdek ve iki hamil ham bloğu hesaplanır. Hamil hacminden çekirdek cebi düşülmez; satın alınacak brüt blok ağırlığıdır. Taslak blokların görsel örtüşmesi tamamlanmış montaj anlamına gelmez.
- Maça ham blokları göz başına tekrarlanabilir. Maça kapsam dışı/yok seçildiğinde teknik olarak üretilmiş maça çelik gideri maliyete eklenmez. Piston ve diğer elle eklenen giderlerin kapsamı ayrıca yönetilir.
- U/V ölçüleri seçilen açılma eksenine diktir. Teklife aktarılan dış zarf, taslak blokların toplam zarfıdır; piston, sürgü mekanizması ve bağlantı zarfları doğrulanmamıştır.

## Maça önerisinin yöntemi ve sınırları

OpenCascade yalnız geçerli kapalı katıları üçgenler; yardımcı eğri/yüzeyler dışarıda kalır. Her yüzün en büyük 64 üçgen havuzundan en fazla 8 uzamsal olarak dağıtılmış üçgen örneği alınır, yüzey normalinde küçük dış ofset uygulanır. X/Y/Z doğrultularındaki ışınlarda iki yönde de engel varsa yüz aday olarak işaretlenir. Erişilebilir yan yönler ve paylaşılan üçgen köşeleri üzerinden bağlantılı yüz grupları ham blok taslağına dönüşebilir. Aday alan oranı en düşük eksen ön öneridir.

Bu, tam bir ters açı/draft veya kalıp açılma analizi değildir. Örnekleme küçük veya yerel bölgeleri kaçırabilir; yüzlerin aynı grupta olması tek bir mekanizma ile çıkarılabilecekleri anlamına gelmez. Sıfır aday, aç-kapa üretim kanıtı değildir. Ayrım düzlemi yalnız parça merkezindeki taslaktır; geometrik ayrım hattı hesaplanmaz. Örneklenmiş normal açıları raporlanır; gerçek imalat çekme açıları, çekinti, alaşım büzülmesi, döküm/yolluk, soğutma, iticiler, maça stroku, piston kuvveti, çarpışma ve dayanım doğrulanmaz. Üretim çizimi/BRep kalıp tasarımı çıktısı yoktur.

Görüntüleme toleransı model boyutuna göre ayarlanır; 100.000 üçgen/3.000 yüz sınırı uygulanır. Üçgenleme gerekirse kabalaştırılır. Orijinal STEP değiştirilmez; görüntüleme önbelleği dosya hash'ine bağlanır ve ZIP'teki orijinalden yeniden üretilebilir. Uç nokta 50 MB/120 saniye ve tek CAD işi sınırındadır.

## Doğrulama

- Node testleri stok, göz yerleşimi, maça tekrarı, brüt kg/bedel, alt maliyet aktarımı ve geçersiz boyutları denetler.
- OpenCascade testleri basit blokta aday oluşmadığını ve açılma yönüne dik delikte maça adayı bulunduğunu doğrular; tam mühendislik doğrulaması sayılmaz.
- Gerçek tarayıcıda WebGL çizimi, döndürme, yüz seçimi, iki nokta ölçümü, kesit, ayrı sağ/sol dosyaları, manuel boyut güncellemesi, maliyete aktarım, görsel kaydı ve önbellekten yeniden açma test edildi.
- Kullanıcının gönderdiği 6,4 MB heatsink STEP gerçek uç noktada 62.228 üçgen ve 1.296 katı yüzüyle açıldı; orijinal geometri korunarak ham kalıp/maça önerileri görüntülendi.

## Taslağı okuma görünümleri

Kalıp yerleşiminde üç görsel ön ayar vardır: Parça yerleşimi yalnız gözlerdeki parçaları gösterir; Ayrılmış kalıp ham blok katmanlarını görsel olarak ayırır; Kapalı kalıp blok zarflarını şeffaf gösterir. Katman aralığı yalnız sahne konumlarına uygulanır, `technical` parametreleri, kg ve bedeller değiştirilmez. Parça/çekirdek/hamil/maça/etiketler ayrı gizlenebilir.

H1/H2 üst-alt hamil, Ç1/Ç2 üst-alt çekirdek, M maça ve G göz kimlikleridir. Sahnedeki kısa kodlar bağlantı çizgileriyle gösterilir; adlar ve gerçek ham blok ölçüleri sabit listede yer alır. Bu, işlenmiş figür cepleri olan bir kalıp modeli değil ham malzeme taslağıdır. Sahnedeki ayrılma mesafesi gerçek kalıp ölçüsü veya maça stroku değildir.

## Düzenlenebilir sağ ölçü paneli ve hareket

Sağdaki hızlı panelde hamil U/V ve iki yarının toplam kalınlığı, her çekirdeğin ham blok ölçüleri, seçilen maçanın U/V/kalınlık/strok değerleri düzenlenir. Hamil toplam kalınlığı iki eşit yarıya bölünür. Manuel düzenleme 3D ve kg/ham bedel hesabını günceller; fiyat tanımlanmamışsa bilinen bedel toplam maliyet değildir. Kalıcı teklif aktarımı “Ölçü ve malzemeleri teklife uygula” ile yapılır.

Maçalar seçilen dünya ekseni yönünde strok kadar birlikte hareket eder. Önerilen strok parça zarfını terk etme mesafesi +5 mm'dir ve değiştirilebilir. 40 konumda eksenlere paralel kutuların ilave hacim girişleri aranır; kapalı konumdaki mevcut temaslar başlangıç kabul edilir. İşlenmemiş hamil/çekirdek cepleri kontrol edilmez. Bu bir CAD çarpışma doğrulaması değildir. Hareket gösterimi stok ölçülerini değiştirmez.

Üst/ön/yan ortografik görünüşler, dış zarf ölçü çizgileri ve blok ölçü/kg tablosu Türkçe veya İngilizce gerçek PDF olarak indirilir. PDF o anki düzenlenmiş taslağı kullanır; ayrılmış gösterim ve hareket pozu ölçülere katılmaz. Dosya tarayıcı indirme klasörüne gider; teklif ölçülerinin kaydı ayrıca Uygula gerektirir. Görünüşler imalat ölçeğinde değildir. PDF üretimi ReportLab ve depodaki lisanslı DejaVu fontlarını kullanır.

## Taraflar ve satın alma payları

Sabit/hareketli çekirdek ve hamiller U/V/kalınlık, çelik adı, yoğunluk ve EUR/kg için ayrı düz alanlar taşır (`fixedInsertDepth`, `movingInsertPrice` gibi); eski kayıtlar ortak değerlere geri düşer. Tarafa ait boyut boşsa ortak hesap kullanılır. Otomatik hesaba dön düğmesi tarafa özel boyutu kaldırır. Hamilin otomatik boyutu kendi tarafındaki çekirdeği izler. Başlangıç ve güncel hesap karşılaştırması ekran açılışını esas alır; fiyat eksikse tam bedel farkı üretilmez.

Her blok için taslak `size` ile satın alma `stockSize` ayrıdır. U/V/W payları iki yüzün toplam ilavesidir, sıfır varsayılanıyla başlar; yoğunlukla kg satın alma boyutundan hesaplanır. Taslak kütlesi de ayrı gösterilir (işlenmiş parça net ağırlığı değildir). 3D taslak paylarla şişirilmez. Maça payları tüm maça bloklarına uygulanır. PDF tablosu satın alma ölçülerini ve kg'ını, açıklamasında taslak ölçüsünü taşır.

Teklife aktarımda sabit çekirdek satın alma ölçüsü bir adet malzeme olarak, hareketli çekirdek ve her hamil ayrı üretilen maliyet satırları olarak yazılır; böylece iki farklı çelik ve fiyat korunur ve çift sayılmaz. Eski, taraf ayrımı olmayan otomatik kayıtların aktarım yolu korunur.

## Maliyet açıklamaları, katalog tarihleri ve gerçek giderler

Her alternatifin maliyet bölümündeki “Nasıl hesaplandı?” alanı ham çelik kg formülünü, kayıtlı miktar × birim bedel satırlarını, fiyat kaynaklarını ve maliyet üzerine kâr/trim hesaplarını gösterir. Excel tabanlı işçilik kuralları dosya gelene kadar bağlı değildir.

Çelik/piston katalog fiyatları değiştirildiğinde `updatedAt` saklanır. Aynı fiyat tekrar kaydedilince tarih değişmez; eski tarihsiz kaydın geçmişi uydurulmaz. Güncel katalog tarihi ile teklife aktarılmış kaynak tarihi ayrı gösterilir. Güncel fiyatlarla hesaplama mevcut alternatifi değiştirmez; önceki revizyon/alternatif korunur. Yeni hesap eski gerçekleşen gider kaydını devralmaz.

`actualCosts` her alternatifte çelik, piston, işçilik ve diğer gerçekleşen EUR giderlerini, notu, kayıt tarihini ve ilk kayıt anındaki maliyet tahminini saklar. Eksik alan sıfır sayılmaz; toplam ancak tüm gruplar tamamlanınca çıkar. Fark gerçekleşen eksi tahmindir. Bu alanlar teklif onayı parmak izinin dışında tutulur ve müşteri çıktısına eklenmez. Kayıtlar normal şirket klasörü/JSON/ZIP arşiviyle taşınır ve geri yüklemede doğrulanır. Kural değişikliği otomatik yapılmaz.
