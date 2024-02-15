#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <MFRC522.h>
#include <SPI.h>


#define RESET 22
#define SDA 5
#define SCK 18
#define MOSI 23 
#define MISO 19


MFRC522 rfid(SDA, RESET); 

byte NUID[4];   // Inicijalizacija array-a za spremanje novih NUID-a 


// const char* SSID = "Marko";
// const char* PASSWORD = "44marko44";

// const char *serverName = "http://127.0.0.1/provjera";
// HTTPClient http;

// StaticJsonDocument<200> doc;


void setup() {
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init(); // Inicijlizacija MFRC522



    // WiFi.begin(SSID, PASSWORD);
    // Serial.print("Connecting to WiFi ..");
    // while (WiFi.status() != WL_CONNECTED) {
    //     Serial.print('.');
    //     delay(500);
    // }
    // Serial.println(WiFi.localIP());
}

void loop() {
    // Resetiraj petlju ako kartica nije u blizini čitača. Stavlja proces u stanje mirovanja.
    if ( ! rfid.PICC_IsNewCardPresent())
        return;

    // Provjerava je li NUID pročitan
    if ( ! rfid.PICC_ReadCardSerial())
        return;

    String id = "";
    // Pretvaranje pročitane vrijednosti u string i dodavanje razmaka između dijelova UID-a
    for (int i = 0; i < rfid.uid.size; i++){
        id += rfid.uid.uidByte[i] < 0x10 ? " 0" : " ";
        id += String(rfid.uid.uidByte[i], HEX);
    }

    id.remove(0, 1); // Brisanje umetnutog prvog razmaka prije UID-a
    Serial.print("UID: ");
    Serial.println(id);
    delay(1000);



    // String temperatura = "22";
    // doc["temperatura"] = temperatura;

    // String json;
    // serializeJson(doc, json);
    // http.begin(serverName);
    // http.addHeader("Content-Type", "application/json");
    
    // int httpResponseCode = http.POST(json);

    // Serial.print("Status code: ");
    // Serial.println(httpResponseCode);
    // Serial.println(http.getString());

    // http.end();
    // delay(10000);
}
