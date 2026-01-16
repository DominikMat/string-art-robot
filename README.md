# String Art Robot

A machine to automatically draw string art designs on a circular ring of nails.

## Project Overview

**Team Members:** 
Dominik Matuszczyk (PL)
Dizha Oleksii (UA) 
Tkachuk Nikita (UA)

This robot was created for the Intro to Robotics course at the University of the Aegean (Fall Semester 2025/26) during our Erasmus trips. 
The system uses a computer-generated sequence to physically wind string around a ring of nails to create geometric patterns.

---

## 🔌 Hardware Wiring
The wiring involves connecting the Servo directly to the Pico and the Stepper Motor via the ULN2003 driver chip.

### Wiring Diagram Table

| Servo connections | Servo Wire colour | Pico Pin | Description |
| :--- | :--- | :--- | :--- |
| (MG996R) | Orange (Signal) | Pico GP16 | PWM Control |
| | Red (VCC) | Pico VBUS | 5V Power |
| | Brown (GND) | Pico GND | Ground |

| Stepper Driver chip connections | ULM Chip Input | Pico Pin | Description |
| :--- | :--- | :--- | :--- |
| (ULN2003) | Pin 1 (IN1) | GP18 | Input for Coil A |
| (Pico to Driver)| Pin 2 (IN2) | GP19 | Input for Coil B |
| | Pin 3 (IN3) | GP20 | Input for Coil C |
| | Pin 4 (IN4) | GP21 | Input for Coil D |
| | Pin 8 (-) | GND | Ground |
| | Pin 9 (+) | VBUS | 5V Power |

| Stepper Motor connections | Stepper Wire colour | ULM Chip Output | Description |
| :--- | :--- | :--- | :--- |
| (28BYJ-48) | Blue | Pin 16 (OUT1) | Coil A |
| (Stepper to driver) | Pink | Pin 15 (OUT2) | Coil B |
| | Yellow | Pin 14 (OUT3) | Coil C |
| | Orange | Pin 13 (OUT4) | Coil D |
| | Red | Pico VBUS | 5V Power |

---

## 🛠️ Software Installation & Setup

To run the robot, you need to set up the PlatformIO environment in VS Code.

### Step 1: Install VS Code & PlatformIO
1. Download and install Visual Studio Code.
2. Open VS Code, go to the Extensions tab (Ctrl+Shift+X).
3. Search for "PlatformIO IDE" and click Install.
4. Restart VS Code once the installation is complete.

### Step 2: Import / Create the Project
To be able to flash the code you can either import or create a PlatformIO project.

IMPORT
1. Download this repository and unzip
2. In the VS Code extension bar click PlatformIO (alien) icon
3. Navigate to Quick Access / PIO Home / Open and click
4. Click the 'Import Arduino Project' Button
5. Choose 'Raspberry Pi Pico' board and the unziped repository directory

CREATE NEW
1. Click the PlatformIO (Alien icon) on the left sidebar.
2. In the VS Code extension bar click PlatformIO (alien) icon
3. Navigate to Quick Access / PIO Home / Open and click
4. Click 'New Project'
3. Name: StringArtRobot
4. Board: Raspberry Pi Pico
5. Framework: Arduino
6. Click Finish.

### Step 3: Configure platformio.ini
If you have created your project as a 'New Project' and not imported it,
make sure the plaformio.ini file matches the configuration below.

```
[env:pico]
platform = raspberrypi
board = pico
framework = arduino
lib_deps = 
    arduino-libraries/Servo@^1.3.0
```

### Step 4: Flash the Code and initalize the board
1. Connect your Raspberry Pi Pico W to the computer via USB.
2. The check button on the bottom of VS Code validates your code (you can immidiately flash the board, but this is faster in case of errors)
3. Flash the Pico board memory with the Right Arrow Icon on the bottom status bar and wait until complete.
4. If successful your Pico board should automatically start executing the code
5. For the initalization protocol of the robot in this project you must next open the serial monitor (the plug icon on the bottom status bar), and then click enter to progress through the steps.
   
---

## 🎨 Pattern Generation (Python)

1. Navigate to the src/ folder.
2. Run: python string_visualizer.py (if you dont have you must install Python 3)
3. The program will display the design in a window. Press SPACE or ENTER to cycle through patterns.
4. The numerical nail sequence will print to your terminal.
5. Copy that sequence and paste it into the "nailSequence" array in your main.cpp before flashing.

---

## Links & Media
* Project Presentation: https://docs.google.com/presentation/d/1VIfVSTO9Wcaq9Rl0Zi-_Bw-y_5G3Nwj30t2qu21ZTrM/edit?usp=sharing
* Demo Video: https://drive.google.com/file/d/1XwlmAQR4rs1_c6xqZL0Uokjqz6scIsDI/view?usp=drivesdk
