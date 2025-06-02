#include <Servo.h>

const byte thrusterPins[9] = {5, 10, 7, 9, 6, 8, 11, 12, 13};  
Servo servos[9]; 

// Thruster mapping:
// servos[0] = T1: Front Top (D5)
// servos[1] = T2: Back Left (D10)
// servos[2] = T3: Front Left (D7)
// servos[3] = T4: Back Right (D9)
// servos[4] = T5: Front Right (D6)
// servos[5] = T6: Back Top (D8)
// servos[6] = CS1: Turning Claw (D11)
// servos[7] = CS2: Opening/Closing Claw (D12)
// servos[8] = CamServo: Camera Servo (D13)

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(10); 

    for (int i = 0; i < 9; i++) {
        servos[i].attach(thrusterPins[i]);
        servos[i].writeMicroseconds(1500);  
    }
    
    delay(2000);
}

void loop() {

    if (Serial.available() > 100) {
        while(Serial.available()) Serial.read();
    }
    
   
    if (Serial.available() > 12) { 
        String inputString = Serial.readStringUntil('\n');
        
        int values[9] = {1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500};
        
        int commaIndex = 0;
        int valueIndex = 0;
        
        for (int i = 0; i < 9 && commaIndex >= 0 && valueIndex < inputString.length(); i++) {
            commaIndex = inputString.indexOf(',', valueIndex);
            if (commaIndex < 0 && i < 8) {
                break;
            }
            
            String valStr;
            if (commaIndex < 0) {
                valStr = inputString.substring(valueIndex);
            } else {
                valStr = inputString.substring(valueIndex, commaIndex);
                valueIndex = commaIndex + 1;
            }
            
            int val = valStr.toInt();
            
            if (val >= 1100 && val <= 1900) {
                values[i] = val;
            }
        }
        
        for (int i = 0; i < 9; i++) {
            servos[i].writeMicroseconds(values[i]);
        }
    }
    
    delay(10);
}
