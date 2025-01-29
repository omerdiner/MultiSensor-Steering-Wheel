#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

//  dokunma sensorunun bagli oldugu pinler
#define NUM_SENSORS 12
const int TTP223_PINS[NUM_SENSORS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};

//  instance of the MAX30100 Pulse Oximeter
PulseOximeter pox;

// LM35 sıcaklık sensörü
const int lm35Pin = A7; //  bağlı olduğu analog pin
float temperatureC = 0;

// Nabız sensörü verileri
float beatsPerMinute = 0;
float spo2 = 0;
float bpmHistory[10] = {0}; // Son 10 nabız verisi
int bpmIndex = 0;
int bpmCount = 0;

// Sabitler ve değişkenler
const int IGNORE_FIRST_N_MEASUREMENTS = 5; // İlk 5 ölçümü yok sayıyoruz
int ignoredMeasurements = 0;
float smoothedBPM = 70; // Başlangıç için ortalama bir BPM değeri
const float SMOOTHING_FACTOR = 0.1; // Hareketli ortalama için katsayı


unsigned long previousMillis = 0;
const long interval = 1000; // 1 saniye aralıklarla veriyi yazacağız

void onBeatDetected() {
  if (ignoredMeasurements < IGNORE_FIRST_N_MEASUREMENTS) {
    ignoredMeasurements++;
    return; // İlk N ölçümü yok say
  }

  float currentBPM = pox.getHeartRate();
  
  // Hareketli ortalama uygulayarak BPM'i güncelliyoruz. amac tutarlı bir nabız göstermek
  smoothedBPM = smoothedBPM * (1.0 - SMOOTHING_FACTOR) + currentBPM * SMOOTHING_FACTOR;

  // Algılanan nabız verisini diziye kaydet
  bpmHistory[bpmIndex] = smoothedBPM;
  bpmIndex = (bpmIndex + 1) % 10; 
  if (bpmCount < 10) {
    bpmCount++;
  }
}

float calculateAverageBPM() {
  if (bpmCount == 0) {
    return 0; // Hiç veri yoksa 0 
  }
  float sum = 0;
  for (int i = 0; i < bpmCount; i++) {
    sum += bpmHistory[i]; 
  }
  return sum / bpmCount;
}

void setup() {
  //  serial monitoru başlatır
  Serial.begin(9600);
  while (!Serial); // seri port hazır olana kadar bekler

  //  TTP223 pinlerini input olarak başlat
  for (int i = 0; i < NUM_SENSORS; i++) {
    pinMode(TTP223_PINS[i], INPUT);
  }

  // MAX30100 sensoru baslat
  Wire.begin();
  Serial.println("MAX30100 sensörü başlatılıyor.");
  if (!pox.begin()) {
    Serial.println("MAX30100 bulunamadı! Bağlantıları kontrol edin.");
    while (1);
  }
  pox.setOnBeatDetectedCallback(onBeatDetected);
  Serial.println("MAX30100 başlatıldı.");
}

void loop() {
  // MAX30100 sensörü verisini güncelle
  pox.update();

  // Zaman kontrolü
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // LM35 sıcaklık sensörü verisini oku
    int sensorValue = analogRead(lm35Pin);
    float voltage = sensorValue * (5.0 / 1023.0); // 5V Arduino için
    temperatureC = voltage * 100.0; // LM35: 10mV = 1°C

    // dokunma sensörü verileri için dizi
    int touchData[12] = {0}; 

    // sensörlerden verileri okur ve diziye aktarır
    touchData[0] = digitalRead(TTP223_PINS[0]);
    touchData[11] = digitalRead(TTP223_PINS[1]);
    touchData[10] = digitalRead(TTP223_PINS[5]);
    touchData[9] = digitalRead(TTP223_PINS[2]);
    touchData[8] = digitalRead(TTP223_PINS[3]);
    touchData[7] = digitalRead(TTP223_PINS[11]);
    touchData[6] = digitalRead(TTP223_PINS[4]);
    touchData[5] = digitalRead(TTP223_PINS[6]);
    touchData[4] = digitalRead(TTP223_PINS[8]);
    touchData[3] = digitalRead(TTP223_PINS[7]);
    touchData[2] = digitalRead(TTP223_PINS[9]);
    touchData[1] = digitalRead(TTP223_PINS[10]);

    // dokunma verisini string haline çeviriyoruz
    String touchBinary = "";
    for (int i = 0; i < 12; i++) {
      touchBinary += touchData[i];
    }

    // nabzı integer olarak alyoruz
    int averageBPM = (int)calculateAverageBPM(); 

    // yazdıracağımız çıktıyı hazırlıyoruz
    String output = touchBinary + "";
    output += " " + String(temperatureC, 1) + " " + String(averageBPM);

   
    Serial.println(output);
  }
}
