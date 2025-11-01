from driver.py import ST7789
import time

def main():
    try:
        display = ST7789()
        colors = [0xf800, 0xfce0, 0xffe0, 0x07e0, 0x023f, 0x001f, 0xf81f]
        i = 0
        while(i<7):
            time.sleep(0.2)
            display.fill(colors[i])
            i = (i+1)%7
    except KeyboardInterrupt:
        print('\n')
    except:
        print('err')
    finally:
        print('cleanup')
        display.cleanup()

if __name__ == "__main__":
    main()
