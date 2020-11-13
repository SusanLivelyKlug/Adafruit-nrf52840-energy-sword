# Adafruit-nrf52840-energy-sword
Internals for an energy sword, two strips of neopixels and sound output controlled by Adafruit Bluefruit app.

**BOM**

Included BOM sheet has the Build materials list and estimated prices for future project quoting only. Prices as of mid 2020, not including shipping/handling.  SDMG donated the strip of neopixels for this build and Susan is donating the remainder of the materials through Make Lively.

**Code**

Software is provided as-is with documentation, including how to do a complete re-install.  The code is creative commons and can be used in other projects that are sold, but cannot be sold as just the software.
Please keep the credits in any code rewrite.  

**How to use the Adafruit Bluefruit app**

In the app store search for Bluefruit Connect, by Adafruit Industries.  Install.  Not yet tested with Apple mobile device. 

**Connecting**

- On the sword handle, slide the switch on the sword to the on position. 
- If the battery is drained then ensure you are plugged into a usb power supply.
- On your mobile, click on the Bluefruit Connect app icon
- Locate ‘Bad Ass Halo Energy Sword’ <working name>
- Click connect button, Sword should show solid blue for a moment to indicate BLE connection

The only coded options for this project are ‘Controller’ -> ‘Control Pad’ or ‘Color Picker’

**Color Picker**

The color picker allows you to scroll around the color circle, as well as select tint and shade.  Once you like the color in the box at the bottom, then click the select button.  The entire strip should be the one color and not showing any animation.

**Control Pad**

When choosing the Control Pad you will be faced with a button dashboard.
1. Button 1 : Turn on / off the animation.  Single clicks only. Bluefruit will remember queued up clicks and run through them all.
2. Button 2 : Blue pulsing animation.
3. Button 3 : Sword swoosh sound and green light animation
4. Button 4 : Pulse sound and orange to cyan light animation <maybe change this to other light combo>
5. Arrow Right and Left:  Scroll through the 5 available animations not including lights off.
6. Arrow Up and Down:  <TBD> increase or decrease the brightness of the lights.

**In case of Re-build**
In the case of needing to replace the feather nrf52840 board, or reinstall the software you can find an installation list in the attached BOM sheet.

**Bugs / Incomplete features**
- Arrow up and down would ideally change the maximum brightness within a reasonable range.
- Left arrow doesn’t circle around 
- More animations would be cool, 4 best on the 1-4 buttons, and the rest only through scrolling?
- Before installation in the final piece there will sometimes be a whine from the speaker / amp.  I am not sure how this happens or how to fix.  Moving the parts around or connecting with BLE seems to fix this whine. Re-evaluate once in the art piece.  Need a sound expert?
- There is always a little amp coming on tic sound.  This is the nature of the code for playing sounds.  More work could perhaps silence this tic. (same expert as in #3 above?)
