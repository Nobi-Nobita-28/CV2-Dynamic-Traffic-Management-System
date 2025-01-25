int greenled = 12;
int redled = 10;

const int vehicleThreshold = 10;
const int peopleThreshold = 5;

int people_count = 0;
int vehicle_count = 0;
int crowd = 10
int traffic = 10;

void setup() {
  
  pinMode(greenled, OUTPUT);
  pinMode(redled, OUTPUT);

  
  Serial.begin(9600);  
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    
    int commaIndex = data.indexOf(',');
    peopleCount = data.substring(0, commaIndex).toInt();
    vehicleCount = data.substring(commaIndex + 1).toInt();
   
    if(default){

    }
    else if(people_count >= crowd && vehicle_count < traffic){
            digitalWrite(redled, HIGH);
            // Red Light
            // digital
            delay(35);
    }
    else if(vehicle_count >= traffic && people_count < crowd){
            Green Light
            delay
    }
    else if(){

    }
  }
}


