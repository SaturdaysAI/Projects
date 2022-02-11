//ConciencIA Ecológica
//Autor:Carlos_Gonzalez - TEAM_Naramja
// Se controla el giro de los servos usando potenciometros estos mediante
//una conversion genera una proporcionalidad con respecto al angulo de giro
//los ultrasonicos sirven para el proceso de medir el nivel de contnedor 
//estos tiene un swith como enable para que no exista interferencia con el giro del servo
//las luces pilotos indican cuando un servo se esta moviendo es decir la apertura o cierre.

#include <Servo.h> // Incluir la librería Servo
Servo servo1; // Crear un objeto tipo Servo llamado servo1
Servo servo2; // Crear un objeto tipo Servo llamado servo2
Servo servo3; // Crear un objeto tipo Servo llamado servo3
Servo servo4; // Crear un objeto tipo Servo llamado servo4
Servo servo5; // Crear un objeto tipo Servo llamado servo5
Servo servo6; // Crear un objeto tipo Servo llamado servo6 
int const PotPin1=A0;
int const PotPin2=A1;
int const PotPin3=A2;
int const PotPin4=A3;
int const PotPin5=A4;
int ledRed1=11;
int ledAmarillo1=12;
int ledVerde1=13;
int trigPin = 9;    
int echoPin = 8; 
int servoPin = 10;
int PotVal1;
int PotVal2;
int PotVal3;
int PotVal4;
int PotVal5;
int angle1;
int angle2;
int angle3;
int angle4;
int angle5;
long duration, dist, verage;   

long aver[3]; 



void setup()
{
 servo1.attach(5) ; // Conectar servo1 al pin 5
 servo2.attach(4) ; // Conectar servo2 al pin 4
 servo3.attach(3) ; // Conectar servo3 al pin 3
 servo4.attach(2) ; // Conectar servo4 al pin 2
 servo5.attach(6) ; // Conectar servo4 al pin 6
 servo6.attach(10) ; // Conectar servo4 al pin 10
 Serial.begin(9600);
 servo6.attach(servoPin);  
 pinMode(trigPin, OUTPUT);  
 pinMode(echoPin, INPUT);  
 servo6.write(0);         
 delay(100);
 servo6.detach(); 

}
void measure() {  
    digitalWrite(10,HIGH);
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(15);
    digitalWrite(trigPin, LOW);
    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH);
    dist = (duration/2) / 29.1;    
}
void loop(){
 
 //Plasticos
  PotVal1=analogRead(PotPin1);
  Serial.print("PotVal1:");
  Serial.print(PotVal1);
  angle1=map(PotVal1,0,1023,0,180);
  Serial.print ("angle= ");
  Serial.println (angle1);
  servo1.write(angle1);
  delay (500);


 //Vidrios
  PotVal2=analogRead(PotPin2);
  Serial.print("PotVal2:");
  Serial.print(PotVal2);
  angle2=map(PotVal2,0,1023,0,180);
  Serial.print ("angle2= ");
  Serial.println (angle2);
  servo2.write(angle2);
  delay (500);

 //Papel/Carton
  PotVal3=analogRead(PotPin3);
  Serial.print("PotVal3:");
  Serial.print(PotVal3);
  angle3=map(PotVal3,0,1023,0,180);
  Serial.print ("angle3= ");
  Serial.println (angle3);
  servo3.write(angle3);
  delay (500);

 //Residuos Organicos
  PotVal4=analogRead(PotPin4);
  Serial.print("PotVal4:");
  Serial.print(PotVal4);
  angle4=map(PotVal4,0,1023,0,180);
  Serial.print ("angle= ");
  Serial.println (angle4);
  servo4.write(angle4);
  delay (500);
  
 //Otros desechos
  PotVal5=analogRead(PotPin5);
  Serial.print("PotVal5:");
  Serial.print(PotVal5);
  angle5=map(PotVal5,0,1023,0,180);
  Serial.print ("angle= ");
  Serial.println (angle5);
  servo5.write(angle5);
  delay (500);
 //Sensor Ultrasonico
  for (int i=0;i<=2;i++){
    //average distance
    measure();               
    aver[i]=dist;            
    delay(10);             
    }
  dist=(aver[0]+aver[1]+aver[2])/3;    

  if ( dist < 12 ) {
    //Change distance as per your need
    servo6.attach(servoPin);
    delay(1);
    servo5.write(0);  
    digitalWrite(ledAmarillo1, LOW);
    digitalWrite(ledRed1, HIGH);
    digitalWrite(ledVerde1, LOW);
    delay(5000);      
    
    servo6.detach();      
  }
  if ( dist > 12 && dist<150 ) {
    //Change distance as per your need
    servo6.attach(servoPin);
    delay(1);
    servo5.write(90);  
    digitalWrite(ledAmarillo1, HIGH);
    digitalWrite(ledRed1, LOW);
    digitalWrite(ledVerde1, LOW);
    delay(5000);      
    
    servo6.detach();
    }
  if ( dist > 150 ) {
    //Change distance as per your need
    servo5.attach(servoPin);
    delay(1);
    servo6.write(90); 
    digitalWrite(ledAmarillo1, LOW);
    digitalWrite(ledRed1, LOW);
    digitalWrite(ledVerde1, HIGH);
    delay(5000);      
  }

}

