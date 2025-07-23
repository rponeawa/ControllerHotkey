import pygame
import subprocess
import time
import pyautogui

PROCESS_NAME = "cemu.exe"

CLOSE_CEMU_BUTTON_1 = 6
CLOSE_CEMU_BUTTON_2 = 7
TOGGLE_FULLSCREEN_BUTTON_1 = 7
TOGGLE_FULLSCREEN_BUTTON_2 = 2

def kill_process_by_name(process_name):
    try:
        command = f'taskkill /F /FI "IMAGENAME eq {process_name}" /T'
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0:
            print(f"终止进程: {process_name}")
        else:
            print(f"终止进程时发生错误: {result.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def main():
    pygame.init()
    pygame.joystick.init()
    joystick = None

    print(f"关闭当前应用：{CLOSE_CEMU_BUTTON_1} (Select) + Button {CLOSE_CEMU_BUTTON_2} (Start)")
    print(f"切换全屏: Button {TOGGLE_FULLSCREEN_BUTTON_1} (Start) + Button {TOGGLE_FULLSCREEN_BUTTON_2} (X)")

    while True:
        try:
            if not pygame.joystick.get_count() and joystick is not None:
                print("手柄断开连接")
                joystick = None

            if joystick is None:
                print("等待手柄连接...")
                while pygame.joystick.get_count() == 0:
                    pygame.joystick.quit()
                    pygame.joystick.init()
                    time.sleep(2)
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                print(f"手柄已连接: {joystick.get_name()}")

            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEREMOVED:
                    print("手柄已被移除")
                    joystick = None
                    break

            if joystick is None:
                continue

            if joystick.get_button(CLOSE_CEMU_BUTTON_1) and joystick.get_button(CLOSE_CEMU_BUTTON_2):
                print("-" * 20)
                pyautogui.hotkey('alt', 'f4')
                print("模拟按下 Alt+F4")
                time.sleep(0.5)
                print(f"终止 {PROCESS_NAME}")
                kill_process_by_name(PROCESS_NAME)
                print("-" * 20)
                time.sleep(2)

            elif joystick.get_button(TOGGLE_FULLSCREEN_BUTTON_1) and joystick.get_button(TOGGLE_FULLSCREEN_BUTTON_2):
                print("-" * 20)
                pyautogui.press('f11')
                print("模拟按下 F11")
                print("-" * 20)
                time.sleep(1)

        except (pygame.error, SystemError) as e:
            print(f"手柄已断开: {e}")
            joystick = None 
            time.sleep(1)

        time.sleep(0.1)

if __name__ == "__main__":
    main()