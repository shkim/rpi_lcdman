import wiringpi
import time

LCD_ROW = 2  # 2 Line
LCD_COL = 16 # 16 Char
LCD_BUS = 4  # Interface 4 Bit mode
LCD_UPDATE_PERIOD = 300 # 300ms

PORT_BUTTON1 = 5
PORT_BUTTON2 = 6

PORT_LCD_RS = 7
PORT_LCD_E  = 0
PORT_LCD_D4 = 2
PORT_LCD_D5 = 3
PORT_LCD_D6 = 1
PORT_LCD_D7 = 4

ledPos = 0
ledPorts = [
    21,
    22,
    23,
    24,
    11,
    26,
    27,
]
MAX_LED_CNT = len(ledPorts)

lcdHandle = 0
lcdDispPos = 0


def system_init():
    # LCD Init
    lcdHandle = wiringpi.lcdInit (LCD_ROW, LCD_COL, LCD_BUS,
        PORT_LCD_RS, PORT_LCD_E,
        PORT_LCD_D4, PORT_LCD_D5, PORT_LCD_D6, PORT_LCD_D7, 0, 0, 0, 0)

    if lcdHandle < 0:
        print("lcdInit failed!")
        return -1

    # GPIO Init(LED Port ALL Output)
    for i in range(MAX_LED_CNT):
        wiringpi.pinMode(ledPorts[i], wiringpi.OUTPUT)
        wiringpi.pullUpDnControl(PORT_BUTTON1, wiringpi.PUD_OFF)

    # Button Pull Up Enable.
    wiringpi.pinMode(PORT_BUTTON1, wiringpi.INPUT)
    wiringpi.pullUpDnControl(PORT_BUTTON1, wiringpi.PUD_UP)
    wiringpi.pinMode(PORT_BUTTON2, wiringpi.INPUT)
    wiringpi.pullUpDnControl(PORT_BUTTON2, wiringpi.PUD_UP)

    return 0


def boardDataUpdate():
    global ledPorts, ledPos, lcdDispPos

    # LED Control
    for i in range(MAX_LED_CNT):
        wiringpi.digitalWrite(ledPorts[i], 0) # // LED All Clear

    wiringpi.digitalWrite(ledPorts[ledPos], 1)
    ledPos += 1

    if ledPos:
        ledPos %= MAX_LED_CNT

    # button status read
    if not wiringpi.digitalRead(PORT_BUTTON1):
        lcdDispPos += 1
    if not wiringpi.digitalRead(PORT_BUTTON2):
        lcdDispPos -= 1


def lcd_update():
    global lcdDispPos, lcdHandle

    lcdFb = [ [ 32 for x in range(LCD_COL) ] for y in range(LCD_ROW) ]
    lcdDispString = [
        #1234567890123456
        " Hello, World! ",
        " LCD 16x2 Demo ",
    ]

    for y in range(LCD_ROW):
        for x in range(LCD_COL):
            fbX = x + lcdDispPos
            if fbX >= 0 and fbX < LCD_COL:
                lcdFb[y][fbX] = ord(lcdDispString[y][x])

    for i in range(LCD_ROW):
        wiringpi.lcdPosition(lcdHandle, 0, i)
        for j in range(LCD_COL):
            wiringpi.lcdPutchar(lcdHandle, lcdFb[i][j])


if __name__ == "__main__":
    wiringpi.wiringPiSetup()
    if system_init() < 0:
        raise SystemExit
    while True:
        time.sleep(LCD_UPDATE_PERIOD / 1000)
        boardDataUpdate()
        lcd_update()
