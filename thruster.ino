
#include <Servo.h>

// Pin definitions forall thrusters and servos
const byte thrusterPins[9] = {5, 10, 7, 9, 6, 8, 11, 12, 13};  
Servo servos[9]; // All servos (thrusters + claw servos + camera)

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
    Serial.setTimeout(10); // Set a short timeout for input processing

    // Initialize all servos to neutral position
    for (int i = 0; i < 9; i++) {
        servos[i].attach(thrusterPins[i]);
        servos[i].writeMicroseconds(1500);  // Neutral position
    }
    
    // Wait for ESCs to initialize
    delay(2000);
}

void loop() {
    // Clear buffer on overflow to avoid processing stale commands
    if (Serial.available() > 100) {
        while(Serial.available()) Serial.read();
    }
    
    // Only process if we have enough data for a complete command
    if (Serial.available() > 12) { // Minimum expected data length
        String inputString = Serial.readStringUntil('\n');
        
        // Use a more robust parsing method
        int values[9] = {1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500}; // Default neutral
        
        // Parse comma-separated values
        int commaIndex = 0;
        int valueIndex = 0;
        
        for (int i = 0; i < 9 && commaIndex >= 0 && valueIndex < inputString.length(); i++) {
            commaIndex = inputString.indexOf(',', valueIndex);
            if (commaIndex < 0 && i < 8) {
                // Not enough values in string, use the last valid one
                break;
            }
            
            String valStr;
            if (commaIndex < 0) { // Last value
                valStr = inputString.substring(valueIndex);
            } else {
                valStr = inputString.substring(valueIndex, commaIndex);
                valueIndex = commaIndex + 1;
            }
            
            // Convert to integer
            int val = valStr.toInt();
            
            // Range checking (safety feature)
            if (val >= 1100 && val <= 1900) {
                values[i] = val;
            }
        }
        
        // Apply values to servos
        for (int i = 0; i < 9; i++) {
            servos[i].writeMicroseconds(values[i]);
        }
    }
    
    // Small delay to prevent excessive CPU usage
    delay(10);
}
