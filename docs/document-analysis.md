# Belge analizi ve 2D ile teklif

Proje belgeleri altındaki “Belgeden talep ve 2D ölçü analizi” panelinde kaynak dosyayı veya yapıştırılmış müşteri talebini seçip analiz edin. EML/TXT, PDF, PNG/JPG/WebP ve DXF desteklenir. PDF metni önceliklidir, metin yetersizse sayfa yerel Tesseract ile okunur. İlk 12 PDF sayfası incelenir; atlanan sayfalar bildirilir. API 30 MB ve 180 saniye sınırındadır. Tesseract `eng` verisi kullanır; Türkçe karakterlerde OCR hataları olabilir.

Çıkarılan belge metni ve her bulgunun sayfası/kaynak alıntısı gösterilir. Açık 1+1 eye/göz ifadesi sağ-sol iki göz olarak, 2 ve 4 cavities gibi ifadeler ayrı alternatifler olarak önerilir. Maça/kızak yok ve trim kapsamı, açık alaşım ve tonaj ifadeleri çıkarılır. Serbest dilin tamamını anlayan bir dil modeli değildir; çelişen ifadeler ve farklı projelere ait kaynaklar kullanıcı tarafından ayrılmalıdır. Belge içeriği talimat olarak çalıştırılmaz.

2D ölçü adayları açık `100 x 80 x 40 mm` veya etiketli uzunluk/genişlik/yükseklik ifadelerinden alınır. Ölçü grubu seçilir, gerekiyorsa düzeltilir ve aynı parça/mm onayı verildikten sonra seçili alternatiflere stok hesabı uygulanır. Çizim sayfası sınırları, piksel boyutu ve DXF çizim sınırları parça ölçüsü sayılmaz. Rastgele tekil ölçülerden görünüş eşleştirme yapılmaz. Belirsiz teknik resimde üç boyut elle tamamlanır; otomatik üretilebilirlik veya maça doğrulaması iddia edilmez. 2D temel kaydı kaynak hash/adını, doğrulanan boyutları ve tarihi saklar. Hayali bir CAD modeli kaydedilmez.

# CAD biçimleri

STEP/STP doğrudan, katı IGES/IGS OpenCascade ile STEP'e çevrilerek aynı görüntüleme ve imza akışında kullanılır. Geçersiz/açık yüzeyli modeller kapalı katı bulunamadığında reddedilir; orijinal dosya korunur. Parasolid X_T/X_B ve CATPart/CATProduct okuyucuları bu depoda bulunmaz. Bu biçimleri analiz etmek için firmanın lisanslı CAD çevirici uygulaması `LS_CAD_CONVERTER_EXECUTABLE` tam yolu ile yapılandırılmalıdır. Adaptör iki argüman alır: girdi dosyası ve çıktı STEP yolu. Node kullanıcı girdisini kabuk komutu olarak çalıştırmaz. 80 saniye çevirme ve 50 MB çıktı sınırı vardır. CATProduct bağımlı montaj dosyaları çeviricide çözümlenmelidir; mevcut tek dosya adaptörü bağımlı dosya paketlerini çözmez. Çevirici yoksa açık hata verilir; kullanıcı STEP/IGES dışa aktarabilir. Kurulmamış çevirici native destek sayılmaz.

`GET /api/capabilities` native CAD biçimlerini ve adaptörün yapılandırılıp yapılandırılmadığını bildirir; adaptör lisansı/kurulumu ayrıca doğrulanmalıdır. DWG için içerik çıkarımı bağlı değildir; DXF veya PDF dışa aktarımı gerekir.
