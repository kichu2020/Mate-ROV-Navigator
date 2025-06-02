import pygame
import serial
import time

class ThrusterController:
    def __init__(self, serial_port='/dev/tty.usbserial-1120', baud_rate=9600):
        print("\n=== Initializing ROV Controller ===")
        pygame.init()
        pygame.joystick.init()

        self.prev_command = ""

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Controller: {self.joystick.get_name()}")
        else:
            raise Exception("No controller found!")

        try:
            self.serial = serial.Serial(serial_port, baud_rate, timeout=0.1)  
            print(f"Connected to PCB on {serial_port}")
            time.sleep(2)
            self.send_command("1500,1500,1500,1500,1500,1500,1500,1500,1500\n") 
        except serial.SerialException as e:
            raise Exception(f" PCB connection failed: {e}")

    def controller_test(self):
        print("\n=== Controller Test Mode ===")
        dead_zone = 0.05  
        clock = pygame.time.Clock()

        try:
            while True:
                pygame.event.pump()

                fb = -self.joystick.get_axis(1)   # Left stick Y → forward/back
                yw = self.joystick.get_axis(0)    # Left stick X → yaw (turn)
                vt = -self.joystick.get_axis(3)   # Right stick Y → vertical

                fb = 0 if abs(fb) < dead_zone else fb
                yw = 0 if abs(yw) < dead_zone else yw
                vt = 0 if abs(vt) < dead_zone else vt

                t1 = t6 = 1500 + int(vt * 400)

                t3 = 1500 + int(fb * 400 - yw * 200)
                t5 = 1500 + int(fb * 400 + yw * 200)
                t2 = 1500 + int(-fb * 400 - yw * 200)
                t4 = 1500 + int(-fb * 400 + yw * 200)

                clamp = lambda v: max(1100, min(1900, v))
                t1 = clamp(t1); t2 = clamp(t2); t3 = clamp(t3)
                t4 = clamp(t4); t5 = clamp(t5); t6 = clamp(t6)

                turn = 1300 if self.joystick.get_button(4) else 1700 if self.joystick.get_button(5) else 1500
                grip = 1300 if self.joystick.get_button(6) else 1700 if self.joystick.get_button(7) else 1500

                cam = 1500
                if self.joystick.get_numhats() > 0:
                    dpad = self.joystick.get_hat(0)
                    if dpad[1] > 0: cam = 1700
                    elif dpad[1] < 0: cam = 1300

                command = f"{t1},{t2},{t3},{t4},{t5},{t6},{turn},{grip},{cam}\n"

                if command != self.prev_command:
                    self.send_command(command)
                    self.prev_command = command

                clock.tick(30)  # 30 FPS

        except KeyboardInterrupt:
            print("\n=== Stopped ===")
            self.send_command("1500,1500,1500,1500,1500,1500,1500,1500,1500\n")
        finally:
            self.close()

    def send_command(self, command):
        try:
            if self.serial.is_open:
                self.serial.write(command.encode('utf-8'))
        except Exception as e:
            print(f"Serial write error: {e}")

    def close(self):
        self.send_command("1500,1500,1500,1500,1500,1500,1500,1500,1500\n")
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
        pygame.quit()

if __name__ == "__main__":
    try:
        controller = ThrusterController('/dev/tty.usbserial-1120')
        controller.controller_test()
    except Exception as e:
        print(f"\n Error: {e}")
    finally:
        if 'controller' in locals():
            controller.close()

