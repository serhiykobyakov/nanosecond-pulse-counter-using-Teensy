# Short pulse counter for photon counting using Teensy 4.0

## Goal
There is a need for short TTL pulses counter with the following requirements:
* input: 5V, 10ns wide square pulses, there are already established signal line using BNC cable from amplifier-discriminator to receiver (receiver has 50 Ohm input)
* counter must be able to count pulses in measuring intervals from 0.05 to 4 seconds
* counter must release warning sound when measuring signal exceed certain allowed value
* communication with PC via USB port

The third demand needs some explanation. When dealing with photomultipliers one have to take necessary precautions to protect photocathode from intense illumination which can cause damage to the device. It is a matter of conscious operation, of cause, one must not expose photomultiplier unintentionally to intense illumination. It is time-consuming, distracting and necessary procedure for humans. The counter may help operator with this by making a sound when the signal level rize above certain threshold. This way, the operator can focus on the measurement and receive an immediate audible warning of a high signal level.

## Step by step implementation

### Project scoping

OK, let's clarify the numbers:

Input signal is (according to Hamamatsu C9744 PHOTON COUNTING UNIT, which is actually preamplifier-discriminator (shame, Hamamatsu, shame!)):

- 5V TTL
- single pulse width 10 ns
- max pulse repetition (linear range): 4·10<sup>6</sup> pulses per second

### The device design

First idea was to get a fast Arduino to count pulses and it was good since it is relatively simple in realization and cheap enough for the device to get born. Let's go bold and get the fastest - Teensy 4.0. And what's more, [frequency counter is already in stock](https://www.pjrc.com/teensy/td_libs_FreqCount.html).

Teensy 4.0 have 3.3V design and 5V pulses are too high for it to be tolarated, so level shifter is necessary. I've been advised to use [74LVC2G17](https://www.ti.com/product/SN74LVC2G17) for that purpose.

To let the device emit sound 5V buzzer is used, powered by 5V from USB line and drived by low switching voltage [IRLB3034 n-channel MOSFET](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/irlb3034/)

The final circuit:

<img src="https://github.com/serhiykobyakov/nanosecond-pulse-counter-using-Teensy/blob/main/circuit.png" alt="drawing" width="600"/>



