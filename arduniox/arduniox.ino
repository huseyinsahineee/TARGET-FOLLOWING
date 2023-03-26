#include <Servo.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

int xPin = A0; 
int yPin = A1;

Servo servo1, servo2;

int xPozisyon = 0;
int yPozisyon = 0;
int otomatik=2;
int tetik=3;
int otoon=4;
int selam=0;
int durumSayac=0;
int step=10;
int pos1, pos2;

void setup() {
  lcd.begin(); 
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);
  pinMode(tetik, INPUT);
  pinMode(otoon,OUTPUT);
  pinMode(otomatik, INPUT);
  servo1.attach(5);
  servo2.attach(6);

  Serial.begin(9600);
}

void loop() {
        
      if(selam == 0){
        lcd.setCursor(0,0);
        lcd.print("    HUSEYIN SAHIN");
        lcd.setCursor(0,1);
        lcd.print("         16290762");        
              
      for(int durumSayac=0; durumSayac <= 18; durumSayac++){
        lcd.scrollDisplayLeft();
        delay(650);
         
      if(durumSayac >= 18){
          selam=1;
          lcd.clear(); 
          }       
          }
        }


  
  if(digitalRead(otomatik) == HIGH){
    
  if (Serial.available() > 0) {
    int y = Serial.parseInt();
    int x = Serial.parseInt();
    int servo1Pos = map(x, 0, 640, 0, 180);
    int servo2Pos = map(y, 480, 0, 0, 180);
    servo1.write(servo1Pos);
    servo2.write(servo2Pos);
      digitalWrite(otoon, LOW);
      int servoangle1=servo1.read();
      int servoangle2=servo2.read();      

    
      lcd.setCursor(0,0);
      lcd.print("X=");
      lcd.print(servoangle2);
      lcd.print((char)223);
      lcd.setCursor(6,0); // İkinci satırın başlangıç noktası
      lcd.print("Y=");
      lcd.print(servoangle1);
      lcd.print((char)223);
      lcd.setCursor(12,0);      
      lcd.print("AUTO");
      lcd.clear();
       
  } 
    else{


      lcd.setCursor(0,0);
      lcd.print("NO TARGET");
      lcd.setCursor(0,1);
      lcd.print("target search");
      for(pos1 = 0; pos1 <= 120; pos1 += step) {   // servo1 taranır
      servo1.write(pos1);
      if(Serial.available() > 0 || digitalRead(otomatik) == LOW){break;}
      for(pos2 = 0; pos2 <= 180; pos2 += step) { // servo2 taranır
      servo2.write(pos2);
      if(Serial.available() > 0 || digitalRead(otomatik) == LOW){break;}
      delay(50); }}



      
    }
    }
    else{
      int servoangle1=servo1.read();
      int servoangle2=servo2.read();
      xPozisyon = map(analogRead(xPin),0,1023,0,180);
      yPozisyon = map(analogRead(yPin),0,1023,0,180);
      lcd.setCursor(0,0);
      lcd.print("X=");
      lcd.print(servoangle2);
      lcd.print((char)223);
      lcd.setCursor(6,0); // İkinci satırın başlangıç noktası
      lcd.print("Y=");
      lcd.print(servoangle1);
      lcd.print((char)223);
      lcd.setCursor(12,0);      
      lcd.print("MANU");
      digitalWrite(otoon, LOW);
      lcd.clear();
      servo1.write(xPozisyon);
      servo2.write(yPozisyon);  
    }
    
}