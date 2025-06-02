#include <Servo.h>

Servo clawServo;
Servo rollServo;

const int CLAW_PIN = 9;
const int ROLL_PIN = 10;

void setup() {
    Serial.begin(9600);
    while (!Serial) {}

    clawServo.attach(CLAW_PIN);
    rollServo.attach(ROLL_PIN);

    clawServo.write(90);
    rollServo.write(90);

    Serial.println("2-Servo Control Ready");
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        int sepIndex = command.indexOf(':');
        if (sepIndex == -1) return;

        String servo = command.substring(0, sepIndex);
        int pos = command.substring(sepIndex + 1).toInt();

        if (pos < 0 || pos > 180) {
            Serial.println("Invalid position");
            return;
        }

        if (servo == "claw") {
            clawServo.write(pos);
            Serial.println("Claw: " + String(pos));
        } else if (servo == "roll") {
            rollServo.write(pos);
            Serial.println("Roll: " + String(pos));
        } else {
            Serial.println("Unknown servo: " + servo);
        }
    }
}
