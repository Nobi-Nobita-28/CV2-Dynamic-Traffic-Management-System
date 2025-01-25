
int red = 12;  
int green = 13;  
int blinkInterval1 = 500;  
int blinkInterval2 = 500;  
int blinkCount1 = 1;  
int blinkCount2 = 1;  

void setup() {
  Serial.begin(9600);  
  pinMode(ledPin1, OUTPUT);  
  pinMode(ledPin2, OUTPUT);  
}

void loop() {
  if (Serial.available() > 0) {
    
    String input = Serial.readStringUntil('\n');
    
    
    int commaIndex = input.indexOf(',');
    if (commaIndex != -1) {
      
      String value1 = input.substring(0, commaIndex);
      String value2 = input.substring(commaIndex + 1);

      
      int peopleCount = value1.toInt();  
      int vehicleCount = value2.toInt();  
      
      
      

      if (peopleCount >= 10 && vehicleCount <= 4) { 
        digitalwrite(red,HIGH);
        delay(40000);
        digitalwrite(red,LOW);
      } 
      else if (peopleCount == 4 && vehicleCount == 15) {  //Traffic
        digitalwrite(green,HIGH);
        delay(100000);
        digitalwrite(green,LOW);
      }
      else if (peopleCount >= 20 && vehicleCount >= 4) {  
        digitalwrite(red,HIGH);
        if(peopleCount == 0){
          digitalwrite(red,LOW);
          continue
        }
        delay(80000);
      }
      else if (peopleCount <= 4 && vehicleCount >= 12) {  //Peak Traffic
        digitalwrite(green,HIGH);
        unsigned long chck_clear = millis();
        while(millis() - chck_clear < greenmaxlimit){
          if(vehicleCount <= 4){
            digitalwrite(green,Low);
          }
        }
        digitalwrite(green,LOW);
      }

      else if(peopleCount >= 15 && vehicleCount >= 8){
        digitalwrite(red,HIGH);
        unsigned long - crowd_chck = millis();
        while(millis() - crowd_chck < redmaxlimit){
          if(peopleCount <= 3){
            digitalwrite(red,LOW);
          }
        }
        digitalwrite(red,LOW);
      }
      else {
          
      }
    }
  }
  
  delay(1000);
}
