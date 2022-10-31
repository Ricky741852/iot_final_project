#include <SPI.h>
#include <LoRa.h>
int counter = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("LoRa Sender");
  if (!LoRa.begin(433E6)) 
  {
    Serial.println("Starting LoRa failed!");
    while(1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  counter++;
  String msg = String(counter);

  Serial.print("Sending message ");
  Serial.println(msg);
  
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
  
  delay(1000);
}
