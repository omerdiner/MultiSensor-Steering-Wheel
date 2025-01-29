# Akıllı Direksiyon Simidi - İleri Sürüş Destek Sistemi

Bu proje, sürüş güvenliğini artırmak için geliştirilmiş bir **akıllı direksiyon simidi** sistemidir. Direksiyon üzerindeki **dokunma sensörleri, sıcaklık sensörleri ve nabız sensörleri** yardımıyla sürücünün fizyolojik ve davranışsal verilerini takip ederek sürüş güvenliğini sağlamak için **görsel ve işitsel geri bildirimler** verir.

---

## 🚀 Özellikler

✅ **Gerçek Zamanlı Veri Takibi**: Sürücünün el pozisyonu, nabız ve sıcaklık değerleri anlık olarak izlenir.  
✅ **Görsel ve İşitsel Uyarılar**: Sensörlerden alınan veriler belirlenen eşik değerlerini aştığında sistem, sürücüyü hem **ekran** hem de **sesli uyarılar** ile bilgilendirir.  
✅ **Sensör Tabanlı Güvenlik**: Direksiyonun doğru kavranıp kavranmadığını analiz eder ve yanlış tutuş durumunda sürücüyü uyarır.  
✅ **Kolay Kullanım**: Kullanıcı dostu arayüz sayesinde veriler **anlık grafiklerle** gösterilir.

---

## 🛠 Donanım Gereksinimleri

Proje, aşağıdaki bileşenlerle çalışmaktadır:

- **Arduino Mega 2560**
- **TTP223B Dokunma Sensörleri (12 adet)**
- **MAX30100 Nabız Sensörü**
- **LM35 Sıcaklık Sensörü**
- **Direksiyon Simidi**
- **Bağlantı kabloları ve jumper setleri**
- **Bilgisayar**

---

## 💻 Yazılım Gereksinimleri

Proje, aşağıdaki yazılım bileşenleri ile geliştirilmiştir:

### **1. Arduino Kodları (`sensor_oku.ino`)**

- Arduino Mega, direksiyon üzerindeki **sensörlerden veri toplayarak** seri port üzerinden bilgisayara iletir.

### **2. Python Arayüz (`wheel_gui4_graphical.py`)**

- **Tkinter** ile görsel bir arayüz geliştirilmiştir.
- **Serial kütüphanesi** ile Arduino’dan gelen veriler işlenir.
- **Sensör verileri analiz edilerek** görsel ve sesli uyarılar oluşturulur.

---

## 🔧 Kurulum ve Kullanım

Bu bölüm, **Arduino kodlarının yüklenmesi** ve **Python arayüzünün çalıştırılması** adımlarını içermektedir.

---

### **1️⃣ Arduino Kodlarının Yüklenmesi**

1. **Arduino IDE’yi indirin ve kurun**: [Arduino Resmi Sitesi](https://www.arduino.cc/en/software) üzerinden en son sürümünü edinin.
2. `sensor_oku.ino` dosyasını **Arduino IDE** ile açın.
3. **Arduino Mega 2560** kartınızı **USB kablo ile bilgisayara bağlayın**.
4. **Araçlar > Kart > Arduino Mega 2560** seçeneğini işaretleyin.
5. **Araçlar > Port > (Bağlı olan COM portunu seçin)**.
6. **Kodları yükleyin** ve seri port üzerinden veri gönderimi başladığında pencereyi açık bırakın.

---

### **2️⃣ Python Arayüzünün Çalıştırılması**

1. **Python 3.x sürümünü yükleyin**: [Python Resmi Sitesi](https://www.python.org/downloads/) üzerinden en son sürümü edinin.
2. **Gerekli kütüphaneleri yükleyin**: Terminal veya Komut İstemi (CMD) üzerinden aşağıdaki komutu çalıştırın:
   ```sh
   pip install pyserial tkinter
   ```
3. **Python arayüz dosyasını çalıştırın**: Terminal veya Komut İstemi’ni açın ve şu komutu girin:

```sh
  python wheel_gui4_graphical.py
```

4. Arduino bağlantısını kontrol edin ve seri portun doğru seçildiğinden emin olun.
5. Program çalıştırıldığında sensörlerden alınan veriler anlık olarak ekranda görünecektir.
6. Yanlış tutuş, yüksek sıcaklık veya nabız gibi anormal durumlar tespit edildiğinde, ekranda uyarı mesajları ve sesli bildirimler verilecektir.
