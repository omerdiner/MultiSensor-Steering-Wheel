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
- **Direksiyon Simidi **
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

### **1️⃣ Arduino Kodlarının Yüklenmesi**
1. `sensor_oku.ino` dosyasını **Arduino IDE** ile açın.
2. **Arduino Mega 2560** kartınızı **USB kablo ile bilgisayara bağlayın**.
3. Kartın **portunu (COM) seçin** ve kodları **yükleyin**.
4. Seri port üzerinden veri gönderimi başladığında kodları kapatmadan **Python arayüzünü çalıştırabilirsiniz**.

### **2️⃣ Python Arayüzünün Çalıştırılması**
1. Python 3.x sürümünü bilgisayarınıza yükleyin.
2. Gerekli kütüphaneleri yüklemek için terminal veya komut satırında aşağıdaki komutları çalıştırın:
   pip install pyserial tkinter
