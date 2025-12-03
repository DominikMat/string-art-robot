#include <Arduino.h>
#include <Servo.h>

/* Ring variables */
const int num_nails = 32; 

/* Stepper variables */
const int motorPin1 = 18; // Blue (IN1)
const int motorPin2 = 19; // Pink (IN2)
const int motorPin3 = 20; // Yellow (IN3)
const int motorPin4 = 21; // Orange (IN4)
const int stepper_steps_per_ring_rotation = 4096*4; // 4 to 1 reducion from stepper to ring, stepper has 2048 steps with half-step sequencing
const int steps_per_nail = stepper_steps_per_ring_rotation / num_nails; // divides cleanly to 512 (32 nails)
const int target_stepper_rpm = 10;
const int step_delay_microseconds = (60/target_stepper_rpm) * 1000 * 1000 / 4096; // calculate delay in um  
int current_ring_step_position = 0;

/* Servo variables */
const int servoPin = 16; 
const int servo_middle_angle = 90;
const int servo_rotation_angle_span = 60;
const int servo_inside_angle = servo_middle_angle + servo_rotation_angle_span/2;
const int servo_outside_angle = servo_middle_angle - servo_rotation_angle_span/2;
const int SERVO_DELAY_MS = 500;

Servo myServo;
int current_servo_angle = 90;
int current_step_index = 0;

const int double_bounce_star_sequence[] = { 0, 11, 28, 7, 24, 3, 20, 31, 16, 27, 12, 23, 8, 19, 4, 15, 0 };
const int double_bounce_star_sequence_len = 17;

// Sekwencja Half-step (8 kroków) - Działająca wersja
const int lookup[8][4] = {
  {1, 0, 0, 0}, {1, 1, 0, 0}, {0, 1, 0, 0}, {0, 1, 1, 0},
  {0, 0, 1, 0}, {0, 0, 1, 1}, {0, 0, 0, 1}, {1, 0, 0, 1}
};

void rotate_ring(int steps, bool anti_clockwise = true) {
    for (int i = 0; i < steps; i++) {
        // one stepper step sequence
        digitalWrite(motorPin1, lookup[current_step_index][0]);
        digitalWrite(motorPin2, lookup[current_step_index][1]);
        digitalWrite(motorPin3, lookup[current_step_index][2]);
        digitalWrite(motorPin4, lookup[current_step_index][3]);

        current_step_index = (current_step_index + (anti_clockwise ? 1 : 7)) % 8; 
        current_ring_step_position = (current_ring_step_position + (anti_clockwise ? 1 : (stepper_steps_per_ring_rotation-1))) % stepper_steps_per_ring_rotation; 
        
        delayMicroseconds(step_delay_microseconds);
    }
}

void moveServo(int targetAngle) {
    if (targetAngle < 0 || targetAngle > 180) {
        Serial.println("Error: angle outside range (0-180deg).");
        return;
    }
    
    // smoothly rotate to target angle
    int step_direction = (targetAngle > current_servo_angle) ? 1 : -1;
    while (current_servo_angle != targetAngle) {
        current_servo_angle += step_direction;
        myServo.write(current_servo_angle);
        delay(5);
    }
    
    delay(SERVO_DELAY_MS);
}

void wait_for_user_confirm() {
    Serial.println("    Confirm goto next setp: (any key): ");
    while (!Serial.available()); // wait until serial input 
    while (Serial.available()) Serial.read(); // clear input buffer
    Serial.println("    Continuing program ...");
}

void rotate_ring_to_nail(int nail_idx) {
    int target_pos = nail_idx * steps_per_nail;
    
    int diff = target_pos - current_ring_step_position;
    if (diff > stepper_steps_per_ring_rotation / 2) diff -= stepper_steps_per_ring_rotation;
    if (diff < -stepper_steps_per_ring_rotation / 2) diff += stepper_steps_per_ring_rotation;

    rotate_ring(abs(diff), diff > 0);
}

void plot_around_nail (int nail_idx) {
    rotate_ring_to_nail (nail_idx);
    moveServo (servo_outside_angle);
    rotate_ring_to_nail ( (nail_idx+1) % num_nails );
    moveServo (servo_inside_angle);
}

void setup() {
  Serial.begin(115200);
  while(!Serial);

  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);

  myServo.attach(servoPin);
  
    // initalize program
    wait_for_user_confirm(); 

    //remove ring    
    Serial.println("");
    Serial.println("Please make sure the nail ring or servo arm is removed");
    wait_for_user_confirm();

    Serial.println("");
    Serial.println("Servo position max anti-clockwise - 0deg");
    moveServo(0); 
    delay(500);
    Serial.println("Servo position max clockwise - 180deg");
    moveServo(180); 
    delay(500);
    Serial.println("Servo position middle - 90deg");
    moveServo(90); 
    delay(500);
    
    Serial.println("");
    Serial.println("Please configure the servo-arm and nail ring to the inital position");
    wait_for_user_confirm();
    delay(1000);
}

void loop() {
    
    Serial.print("");
    moveServo(servo_inside_angle); 
    rotate_ring_to_nail (double_bounce_star_sequence[1]);
    Serial.println("Please attach the string to the starting nail");
    Serial.println("  the nail under the servo arm is number 0");
    Serial.print("  "); Serial.print(double_bounce_star_sequence[1]); Serial.println(" counting clockwise");
    Serial.print("  "); Serial.print(num_nails - double_bounce_star_sequence[1]); Serial.println(" counting couter-clockwise");
    wait_for_user_confirm();
    
    Serial.print("");
    Serial.println("STARTING DRAWING");

    for (int i=1; i<double_bounce_star_sequence_len; i++) {
        Serial.print("    going to next nail - num ");
        Serial.println(double_bounce_star_sequence[i]);

        plot_around_nail ( double_bounce_star_sequence[i] );
    }

    Serial.println("DRAWING COMPLETE");

    while (true) {
        delay(10000); 
    }
}