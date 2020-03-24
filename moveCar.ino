#include <SoftwareSerial.h>
SoftwareSerial SoftSerial(8, 9); // RX, TX

#define in1 2 
#define in2 3 
#define in3 4
#define in4 5

float data = 0.5;
int count = 0;
int counter = 0;
int mode = 3; //mode = 1: Manual; mode = 2: Obstacle Advoidance; mode = 3: Computer Vision
#define delayTime 500

#define echoPin 7 //Echo Pin
#define trigPin 6 //Trigger Pin
#define maximumRange 55 //Maximum range needed
#define minimumRange 0 //Minimum range needed
long duration, distance; //Duration used to calculate distance

/*
 * Car motion Functions
 */
      void TurnMotors_BW(){              
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
      }
      
      void TurnMotors_BW_LFT(){              
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
      }
      
      
      void TurnMotors_RHT(){              
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
      }
      
      void TurnMotors_BW_RHT(){              
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
      }
      
      void TurnMotors_LFT(){              
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
      }
      
      void TurnOFF(){
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);  
        digitalWrite(in4, LOW);
      }
      
      void TurnMotors_FW(){              
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, LOW);  
        digitalWrite(in4, HIGH);
      }
/*
 * Arduino General Functions
 */
void setup() {
  //Initialize The motor "in" pins
      pinMode(in1, OUTPUT); //Declaring the pin modes
      pinMode(in2, OUTPUT); //Declaring the pin modes
      pinMode(in3, OUTPUT); //Declaring the pin modes
      pinMode(in4, OUTPUT); //Declaring the pin modes

  //Initialize the ultrasonic sensor pins
      pinMode(trigPin, OUTPUT);
      pinMode(echoPin, INPUT);
  
  //Initialize the Soft-Serial and Serial Communication
      Serial.begin(19200);
      SoftSerial.begin(9600);
      
          //Print for debugging purpose
              SoftSerial.println("       **** This a Software Serial **** ");
              //Serial.println("       **** This a Hardware Serial **** ");
}

void loop(){

    //MANUAL MODE
    if(mode == 1){
    //Change between modes; do operations depending on the mode
        
        if(SoftSerial.available() > 0){
            char variable1 = SoftSerial.read();  
            if(variable1 == 'M'){
                TurnOFF();
                delay(500);
                mode = 1;
            }
            if(variable1 == 'U'){
                TurnOFF();
                delay(500);
                mode = 2;
            }
            if(variable1 == 'C'){
                TurnOFF();
                delay(500);
                mode = 3;
            }

            //FORWARD
            if(variable1 == 'W'){
                //Serial.println("FWD");
                TurnMotors_FW();
                delay(500);
            }
            
        
            //BACKWARD
            if(variable1 == 'S'){
                //Serial.println("BWD");
                TurnMotors_BW();
                delay(500);
            }
    
            //TURN RIGHT
            if(variable1 == 'D'){
                //Serial.println("RHT");
                TurnMotors_RHT();
                delay(500);
            }
    
            //TURN LEFT
            if(variable1 == 'A'){
                //Serial.println("LFT");
                TurnMotors_LFT();
                delay(500);
            }
                
            if(variable1 == ' '){
                //Serial.println("STOP!");
                TurnOFF();
                delay(500);
            }
        
        }
            
    } //End of MANUAL MODE


    //OBSTACLE ADVOIDANCE MODE
    else if(mode == 2){
        if(SoftSerial.available() > 0){
            char variable1 = SoftSerial.read();  
            if(variable1 == 'M'){
                TurnOFF();
                delay(500);
                mode = 1;
            }
            if(variable1 == 'U'){
                TurnOFF();
                delay(500);
                mode = 2;
            }
            if(variable1 == 'C'){
                TurnOFF();
                delay(500);
                mode = 3;
            }
        }
        
        digitalWrite(trigPin, LOW); 
        delayMicroseconds(2); 
  
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10); 
        digitalWrite(trigPin, LOW);
        long duration = pulseIn(echoPin, HIGH);
  
        //Calculate the distance (in cm) based on the speed of sound.
        long distance = (duration / 2) * 0.0343;
  
        if (distance >= maximumRange || distance <= minimumRange){
              SoftSerial.println("Its good. Go forward!");
              TurnMotors_BW();
              delay(500);
        }
	else {
              int randomnum = random(5);
              SoftSerial.println("There is an obstacle stop or turn other way");
              TurnMotors_FW();
              delay(500);
              if (randomnum >= 3) {
                  SoftSerial.println("TURN LEFT");
                  TurnMotors_LFT();
                  delay(500);
              }
	      else {
                  SoftSerial.println("TURN RIGHT");
                  TurnMotors_RHT();
                  delay(500);
              }
        }
    } //End of OBSTACLE AVOIDANCE MODE
    
    //COMPUTER VISION MODE
    else if (mode == 3){       
        if (SoftSerial.available() > 0) {
            char variable1 = SoftSerial.read();  
            if (variable1 == 'M') {
                TurnOFF();
                delay(500);
                mode = 1;
            }
            if(variable1 == 'U') {
                TurnOFF();
                delay(500);
                mode = 2;
            }
            if (variable1 == 'C') {
                TurnOFF();
                delay(500);
                mode = 3;
            }
        }
        
        if (Serial.available() > 0) {
          data = Serial.parseFloat();  
        }
        
        if (data == 0) {
          counter = 3;
          count = 0;
        }
        else if (data == 0.5) {
          counter = 0;
          count = 0;
        }
        else {
          counter = (data * 500) / 14.6;
          count = 0;
        }
       
        TurnOFF();
        while(count < counter){
            TurnMotors_FW();
            count = count + 1;
            Serial.println(count);
        }
        
        if (count == counter) {
          data = 0.5;
          delay(500);
        }
            
        Serial.println("DONE");
        TurnOFF();
    
    }
   
}
