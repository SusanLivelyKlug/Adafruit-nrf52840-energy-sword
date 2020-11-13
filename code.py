"""
    Halo sword with neopixel strips and sound effects, controlled by Adafruit Bluefruit app.
    Sounds by:
    Code by: Susan Lively Klug
    Original Code parts by: Phil Burgess, Dan Halbert & Erin St Blaine for Adafruit Industries.
    Special thanks to Adafruit's Kattni Rembor and John Parks, their examples and help in picking
	the proper hardware gives me all the feels.  I could not have figured this out without their
	generosity of information.
"""
import time
import board
import neopixel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.helper import PixelSubset
# bluefruit
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket
# audio
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

#-------------------- constants
NUM_LEDS = 20                   # change to reflect your LED strip
NEOPIXEL_PIN = board.D13        # change to reflect your wiring
OFFSET_MAX = 1000000
BRIGHTNESS_MAX = 50
brightness_increment = .1
offset_increment = 1
DEBUG = False

#-------------------- Neopixel and Animation Setup
# Set up a map dividing length of the neopixel strips for color/animation variety
#
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_LEDS, auto_write=False, brightness=.5)
pixel_m1 = PixelSubset(pixels, 0, 5)
pixel_m2 = PixelSubset(pixels, 5, 10)
pixel_m3 = PixelSubset(pixels, 10, 15)
pixel_m4 = PixelSubset(pixels, 15, 20)

#-------------------- name colors
RED = (31, 4, 0, 50)  # orangish red for power on confirmation nice and dull
BLACK = (0, 0, 0, 0)
BLUE = (0, 30, 31, 50) # nice dull cyan blue to indicated BLE connected

#-------------------- To be used?
# Prophets' Bane
P4 = (230, 230, 0, 0)  # 4 is tip
P3 = (255, 155, 0, 0)  #
P2 = (255, 90, 0, 0)
P1 = (255, 55, 0, 0)

#-------------------- Vorpal animation
SIZE = 3
SPACING = 1
# colors
V4 = (0, 255, 90, 0)  # 4 is tip
V3 = (0, 155, 90, 0)  # Cyan
V2 = (50, 90, 75, 0)
V1 = (200, 39, 0, 0)
v1 = Chase(pixel_m1, speed=.15, color=V1, size=SIZE, spacing=SPACING, reverse=True)
v2 = Chase(pixel_m2, speed=.1, color=V2, size=SIZE, spacing=SPACING, reverse=True)
v3 = Chase(pixel_m3, speed=.09, color=V3,size=SIZE, spacing=SPACING, reverse=True)
v4 = Chase(pixel_m4, speed=.08, color=V4, size=SIZE, spacing=SPACING, reverse=True)
def vorpal():
    v1.animate()
    v2.animate()
    v3.animate()
    v4.animate()

#-------------------- Red Pulsing
# colors
R1 = (255, 0, 0, 0)  # 4 is tip
R2 = (211, 10, 0, 0)
R4 = (200, 15, 0, 0)
R3 = (100, 0, 0, 0)
pulse = Pulse(pixels, speed=.2, period=3, color=BLUE)
PPERIOD = 2
PSPEED = .25
pulse_m1 = Pulse(pixel_m1, speed=PSPEED, period=PPERIOD, color=R1)
pulse_m2 = Pulse(pixel_m2, speed=PSPEED, period=PPERIOD, color=R2)
pulse_m3 = Pulse(pixel_m3, speed=PSPEED, period=PPERIOD, color=R3)
pulse_m4 = Pulse(pixel_m4, speed=PSPEED, period=PPERIOD, color=R4)
def map_pulse():
    pulse_m1.animate()
    pulse_m2.animate()
    pulse_m3.animate()
    pulse_m4.animate()

#-------------------- Ravening
# Colors
B4 = (0, 255, 255, 0)  # 4 is tip
B3 = (0, 155, 255, 0)
B2 = (0, 55, 255, 0)
B1 = (0, 0, 255, 0)
# Chase: pixel_object, speed, color, size=2, spacing=3, reverse=False, name=None
SIZE = 3
SPACING = 1
rm1 = Chase(pixel_m1, speed=.07, color=B1, size=SIZE, spacing=SPACING, reverse=True)
rm2 = Chase(pixel_m2, speed=.09, color=B2, size=SIZE, spacing=SPACING, reverse=True)
rm3 = Chase(pixel_m3, speed=.1, color=B3, size=SIZE, spacing=SPACING, reverse=True)
rm4 = Chase(pixel_m4, speed=.15, color=B4, size=SIZE, spacing=SPACING, reverse=True)
def ravening():
    rm1.animate()
    rm2.animate()
    rm3.animate()
    rm4.animate()

#-------------------- Infected
# Colors
G4 = (0, 255, 0, 0)  # 4 is tip
G3 = (0, 155, 0, 0)
G2 = (0, 100, 0, 0)
G1 = (0, 55, 0, 0)
# Comet pixel_object, speed, color, tail_length=0, reverse=False, bounce=False, name=None, ring=False)
TAIL = 6
BOUNCE = False
inf1 = Comet(pixel_m1, speed=.09, color=G1, tail_length=TAIL, bounce=BOUNCE)
inf2 = Comet(pixel_m2, speed=.1, color=G2, tail_length=TAIL, bounce=BOUNCE)
inf3 = Comet(pixel_m3, speed=.08, color=G3, tail_length=TAIL, bounce=BOUNCE)
inf4 = Comet(pixel_m4, speed=.15, color=G4, tail_length=TAIL, bounce=BOUNCE)
def infected():
    inf1.animate()
    inf2.animate()
    inf3.animate()
    inf4.animate()

#-------------------- Animation Loop
# Animation choices based on 4 button choices
# button 1 is on/off (animation 0 or 1)
# button 2 is pulse red
# button 3 is
# button 4 is green comet
MAX_ANIMS = 5  # 0,1,2,3,4
animation_num = 0
def run_animation(animation_num):
    if animation_num == 0:
        pixels.fill(BLACK)
        pixels.show()
    elif animation_num == 1:
        map_pulse()
    elif animation_num == 2:
        ravening()
    elif animation_num == 3:
        infected()
    elif animation_num == 4:
        vorpal()

#-------------------- Bluefruit setup
ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)
scan_response = Advertisement()
scan_response.complete_name = "Bad Ass Halo Energy Sword"

#-------------------- Audio setup
audio = AudioOut(board.A0)  # Speaker
wave_file = None

def play_wav(name, loop=False):
    """
    Play a WAV file in the 'sounds' directory.
    :param name: partial file name string, complete name will be built around
                 this, e.g. passing 'foo' will play file 'sounds/foo.wav'.
    :param loop: if True, sound will repeat indefinitely (until interrupted
                 by another sound).
    """
    global wave_file  # pylint: disable=global-statement
    if DEBUG == True:
        print("playing", name)
    if wave_file:
        wave_file.close()
    try:
        wave_file = open('sounds/' + name + '.wav', 'rb')  # using wave files from sounds folder
        wave = WaveFile(wave_file)
        audio.play(wave, loop=loop)
    except OSError:
        pass  # we'll just skip playing then


#-------------------- variables that may change with buttons
offset = 0  # Positional offset into color palette to get it to 'spin'
brightness = .01
cycling = True
sword_on = False

#-------------------- Run once on startup
print('Hello Halo')
pixels.fill( RED )
pixels.show()
time.sleep(1.5)
pixels.fill(BLACK)
pixels.show()

#-------------------- forever while power
while True:
    print("Sword waiting, connect with Adafruit Bluefruit app")
    was_connected = False

    # Advertise when not connected.
    ble.start_advertising(advertisement,scan_response)

    while not ble.connected:
        if cycling:
            run_animation(animation_num)
        #   set_palette(palette_choice, brightness)
        #   offset = (offset + offset_increment) % OFFSET_MAX

    while ble.connected:
        if not was_connected: # blink blue first time connect
            was_connected = True
            print('BLE inititated\n')
            pixels.fill( BLUE )
            pixels.show()
            time.sleep(1.5)
            run_animation(0) # black out
        if uart_service.in_waiting:
            packet = Packet.from_stream(uart_service)
            if isinstance(packet, ColorPacket):
                cycling = False
                if DEBUG == True:
                    print('Color Packet rxd ', packet.color)
                # Set all the pixels to one color and stay there.
                pixels.fill(packet.color)
                pixels.show()
            elif isinstance(packet, ButtonPacket):
                cycling = True
                if packet.pressed:
                    if DEBUG == True:
                        print('button ', packet.button, 'animation number ', animation_num)
                    if packet.button == ButtonPacket.BUTTON_1:
                        if sword_on:
                            if DEBUG == True:
                                print('sword turning off')
                            sword_on = False
                            animation_num = 0  # black out animation. makes a hum in speaker.
                            play_wav("drop1")
                        else:
                            if DEBUG == True:
                                print('sword turning on')
                            sword_on = True
                            animation_num = 1 # power on
                            # painful play_wav("ready")
                            play_wav("drop1")
                    elif packet.button == ButtonPacket.BUTTON_2:
                        sword_on = True
                        animation_num = 2
                        play_wav("loop1")
                    elif packet.button == ButtonPacket.BUTTON_3:
                        sword_on = True
                        animation_num = 3
                        play_wav("melee_1")
                    elif packet.button == ButtonPacket.BUTTON_4:
                        sword_on = True
                        animation_num = 4
                        play_wav("m_loop")
                    # ?change the speed of the animation by incrementing offset?
                    # ?change the brightness overall?
                    elif packet.button == ButtonPacket.UP:
                        brightness_increment += 1
                        # print("brightness up")
                    elif packet.button == ButtonPacket.DOWN:
                        brightness_increment -= 1
                        # print("brightness down")
                    elif packet.button == ButtonPacket.LEFT:  #move forward through animations
                        offset_increment -= 1
                        animation_num += 1
                        if animation_num > MAX_ANIMS:
                            animation_num = 0  #loop around
                        if DEBUG == True:
                            print("offset_increment ", offset_increment)
                    elif packet.button == ButtonPacket.RIGHT:  #move back through animations
                        offset_increment += 1
                        animation_num -= 1
                        if animation_num < 0:
                            animation_num = MAX_ANIMS  #loop around
                        if DEBUG == True:
                            print("offset_increment ", offset_increment)

        if cycling:
                offset = (offset + offset_increment) % OFFSET_MAX
                brightness = (brightness + brightness_increment) % BRIGHTNESS_MAX
                #  print("offset, brightness ", offset, brightness)
                run_animation(animation_num)