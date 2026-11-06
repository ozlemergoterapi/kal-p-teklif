# Analiz V4 hesap yöntemi

Kullanıcı Analiz_V4.xlsx dosyasını ana formül kaynağı olarak belirledi. Analiz V3 örnekleri yalnız tarihsel toplam fiyat ve işçilik saatleri için referanstır; V3 malzeme birim fiyatları, kâr formülü ve ölçüleri yeni modelin otomatik hesabına aktarılmaz. Dosya adı aynı olsa bile içerik hash'i ve kaynak sayfa ayrı izlenmelidir.

Yeni alternatifler `pricing.method = analiz-v4` ve maliyet hesabı moduyla açılır. Önceden kayıtlı alternatifin yöntemi kendi kaydında kalır; yöntem/parametre değişikliği açık kullanıcı düzenlemesidir ve onay içeriğine katılır. Uygulama V4 yöntemi bulunmayan eski kayıtlarda tek oranlı hesabı korur. Yeni V4 ham blokların başlangıç yoğunluğu kaynak formüllerdeki gibi 8.000 kg/m³; önceden kaydedilmiş yoğunluklar ve seçilen malzeme yoğunluğu korunur.

## İç maliyet ve satış

- İç maliyet = miktar × iç satın alma birim fiyatı.
- Malzeme/ısıl işlem ve kaplama: iç maliyet × (1 + malzeme oranı).
- Piston, hırdavat ve mil/burç: iç maliyet × (1 + hırdavat oranı).
- Saatlik işçilik: saat × iç saat ücreti × (1 + işçilik oranı).
- CAD+CAM ve kalite paketleri, elektrot ve nakliye: kaynakta ayrıca ekleme uygulanmıyor; varsayılan grup “Ek kâr uygulanmaz”. Her satır grubu değiştirilebilir.
- Grupların satır satışları toplanır. Toplam üzerine yeniden kâr eklenmez.

Kaynak sayfalarda malzeme/hırdavat başlangıç oranları %5/%5, işçilik çoğunda %20, bir montaj örneğinde %40. Oranlar Ayarlar'dan ve alternatifte düzenlenir. Tek bir grubun oranı tüm projenin kârı sayılmaz.

İşlem tarifesi seçimi V4'teki iç saat/paket bedellerini getirir; saat miktarı otomatik belirlenmiş sayılmaz. Tarifeler Ayarlar'dan değiştirilebilir. Satırda manuel fiyat değişikliği işaretlenirse yeniden fiyatlandırma bunu sessizce katalog fiyatına döndürmez. Isıl işlem/kaplama kg, hırdavat/piston adedi, boyut ve işleme süresi formüllerde bağımsız girdilerdir; modelden otomatik güvenilir tahmin kuralları kalan referanslar doğrulandıktan sonra ayrıca geliştirilmelidir.

## Doğrulanan farklar

Kaynak Excel kâr göstergesi `satış × (satış/maliyet − 1)` kullanıyor. Kullanıcı gerçek farkın gösterilmesini onayladı. Program gerçek farkı `kullanılan satış − iç maliyet` olarak gösterir; Excel göstergesi karşılaştırma için ayrı adla kalır. Maliyet sıfırsa oran tanımsız gösterilir; sonsuz/yüzde hesabı yapılmaz.

“İnilebilecek min fiyat” kaynakta `iç maliyet × 1,2`. Bazı sayfalarda bu değer formül satışının üstünde. Kaynak sonucu sessizce değiştirmemek için program bunu referans olarak gösterir ve otomatik alt sınır uygulamaz. Oran düzenlenebilir.

Boş miktar/fiyat, üretim için sıfır maliyet gibi kabul edilmez; eksik girdiler otomatik satış tutarını durdurur. Kapsam dışı satırlar açıkça kapatılır. Montaj/yalnız işçilik teklifinde ana çekirdek malzemesi ayrıca kapatılabilir. Geçersiz oran veya sınıflandırılmamış “Diğer” satırı eksik olarak gösterilir.

## Doğrulama

Kullanıcı dosyasının altı sayfasındaki 739 formül bağımsız aritmetik değerlendirmeyle kontrol edildi; kayıtlı sonuçların tümü eşleşti. Ana dosyanın altı sayfası ile ayrıca gelen, kullanıcı tarafından proje hesabı olduğu doğrulanan V4 örneğinin 122 formülü de kontrol edildi (toplam 861 formül). Yedi kaynak senaryonun normalize edilmiş satır tutarlarıyla maliyet, formül satış, referans minimum, gerçek fark ve Excel gösterge karşılığı test edilir. C13/C21 kopya senaryolar ayrı geometri/süre eğitim örneği sayılmaz. Bu testler fiyat aritmetiğini doğrular; maça/yerleşim/işçilik süresi tahmin doğruluğunu kanıtlamaz.

Yeni müşteri örnekleri ve özgün dosyalar Git deposu dışında `project-reviews` altında tutulur. Gerçek parça/salkım ayrımı, iş türü (yeni kalıp / yenileme / montaj / trim) ve kaynak şartlar ayrı doğrulanır.

## Çelik kataloğu

V4 sağ üst referans tablosundan 10 çelik, EUR/kg olarak aktarılır: 2312 2,2; 2344 3,9; W350 12,2; W360 15,8; DIEVAR 9,5; DIE CAST ONE 7,5; 1730 1,5; 2714 2,7; 2343 ESR 4,8; CK45 43/36. Yeni kayıtların başlangıç yoğunluğu 8000 kg/m³'tür. Mevcut fiyat, yoğunluk ve tarih korunur; kaydedilen silmeler yeniden eklenmez. Çelik listesinde ısıl işlem ve kaplama yer almaz; hizmet referansları sırasıyla 2,4 ve 2,7 EUR/kg'dır. Özel teklif satırındaki farklı fiyatları değiştirmez. DH31-EX için fiyat uydurulmaz.

SolidWorks önizlemeleri sayısal CAD çözümlemesi yerine geçmez. Yerleşim ve maça ölçülerinin genellenebilir biçimde kalibre edildiği iddia edilmez; doğrulanmış geometri ve eşleştirilmiş hesap örnekleri gereklidir.

## Arşiv ölçülerinden otomatik taslak önerisi

Yeni V4 taslaklarında `Arşiv ölçülerine göre öner` modu açılır. Önceden kayıtlı teknik taslaklar kendi ölçülerini ve temel modunu korur. Referanslar R01–R04, sağlanan analizlerdeki tam hamil/çekirdek grubu çiftlerinin yalnız sayısal ölçüleridir; müşteri belgeleri uygulamaya kopyalanmaz. Yenileme hesapları ve yalnız plaka grubunu içeren satırlar tam hamil örneği sayılmaz.

Yerleşim ve mevcut kenar kuralıyla çekirdek U/V hesaplanır. Eksenlerin iki sıralamasında, logaritmik boyut farkı en küçük olan referans seçilir. Her iki yönde 0,5–2 aralığı dışında eşleşme kullanılmaz. Pay ve kalınlık için ölçek, alan oranının kareköküdür. Grup kalınlığı iki tarafa eşit bölünerek bir başlangıç önerisi yapılır; gerçek ayrım düzlemi veya plaka görevleri çözülmüş sayılmaz. Referans kodu, kaynak ölçüler, ölçek ve bu varsayım ekranda gösterilir.

Arka, duvar ve taban payları referans modunda alt sınırdır. Doğrudan girilen çekirdek/hamil ölçüleri ve tarafa özel ölçüler önceliklidir; eski teklifler yeniden yazılmaz. Ölçü değişince 3D bloklar, kg ve maliyet yeniden hesaplanır. Temel pay kurallarına dönülebilir.

Maça adayı geometri ile oluşturulduktan sonra, yakın ölçekteki benzersiz maça örnekleriyle boyut önerisi büyütülebilir; gereken geometrik zarf küçültülmez. Bu işlem maça sayısı, çıkarma yönü veya kızak mekanizmasını kanıtlamaz. Eşleşmeyen boyutlarda mevcut geometrik paylar kullanılır. Kızak örnekleri maça ölçüsü diye karıştırılmaz.

## Kullanıcı tercihlerinden yerel ölçü öğrenimi

Teknik ölçüler teklife uygulandığında, geometri, göz sayısı, etkin maçalar ve düzeltilmiş blok ölçülerinin bir örneği aynı teklif içinde saklanır. Onayı geçerli teklifler, yeni taslaklara kişisel referans sağlar. Taslak/bekleyen/iptal veya onayı bozulan teklifler kaynak olmaz; malzeme ölçüleri sonradan değiştirilmiş eski teknik örnekler de kullanılmaz. Aynı modelin aynı göz/düzen/yapı/eksen kombinasyonundaki revizyonlarından yalnız en son onaylanan alınır.

Aynı göz, açılma ekseni, sağ-sol düzeni ve maçalı/maçasız yapı ile her eksende ±%20–25 benzer parça ölçüleri aranır (oran aralığı 0,8–1,25). En yakın en fazla beş örnekten medyan paylar ve ayrı taraf kalınlıkları çıkarılır. Tek veya iki örnek varsa sınırlı örnek uyarısı gösterilir. Kişisel öneri yalnız yeni teknik taslağın başlangıç değerlerine uygulanır; mevcut taslak veya fiyatlar arka planda değişmez. Kaynak teklif kodları ekranda belirtilir.

Bu yapı yerel örnek tabanlı ölçü uyarlamasıdır; bir yapay zekâ modelini yeniden eğitmez. Maça sayısı/yönü, piyasa çelik fiyatı veya işleme saatini otomatik öğrenmiş sayılmaz. Maçalar elle eklenebilir, ölçülendirilebilir, devre dışı bırakılabilir ve kaldırılabilir. Son maça kaldırıldığında maça maliyet satırları ve teklif kapsamı temizlenir. Öğrenme ayarlardan kapatılabilir. Örnekler teklifin parçası olduğundan mevcut yedekleme/kayıt konumu mekanizmasıyla taşınır; uzak bir servise gönderilmez.
