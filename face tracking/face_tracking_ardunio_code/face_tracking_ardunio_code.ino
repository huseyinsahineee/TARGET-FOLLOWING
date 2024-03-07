#include <LiquidCrystal_I2C.h>
#include <Servo.h>
//#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

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
int servoStepDelay = 15;  // Delay between each step in milliseconds
int i;
void setup() {
  lcd.begin(); 
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);
  pinMode(tetik, INPUT);
  pinMode(otoon,OUTPUT);
  pinMode(otomatik, INPUT);
  servo1.attach(9);
  servo2.attach(10);
  servo1.write(90);
  servo2.write(90);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available()) {
    char x =Serial.read();
    int v =Serial.parseInt();
    if(x =='a'){
     servo2.write(v);
    }
    if(x =='b'){
    servo1.write(v);
    }   
}    
}