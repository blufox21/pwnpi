from driver import ST7789
import time

def main():
    try:
        display = ST7789(w=170, h=320, x_off=35)
        gui = Gui(display)
    except KeyboardInterrupt:
        print('\n')
    except:
        print('err')
    finally:
        print('cleanup')
        display.cleanup()

if __name__ == "__main__":
    main()
