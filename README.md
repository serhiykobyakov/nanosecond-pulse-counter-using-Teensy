# Short pulse counter for photon counting using Teensy 4.0

## Goal
There is a need for short TTL pulses counter with the following requirements:
* input: 5V, 10ns wide square pulses, there are already established signal line using BNC cable from amplifier-discriminator to receiver (receiver has 50 Ohm input)
* counter must be able to count pulses in measuring intervals from 0.05 to 4 seconds
* communication with PC via USB port
* counter must release warning sound when measuring signal exceed certain allowed value

The last demand needs some explanations. When dealing with photomultipliers one have to take necessary precautions to protect photocathode from intense illumination which can cause damage to the device. It is a matter of conscious operation, of cause, one must not expose photomultiplier to intense illumination (unintentionally). It is time-consuming, distracting and necessary procedure for operator. The counter may help the operator with this by making a sound when the signal level rise above certain threshold. This way, the operator can focus on the measurement and receive an immediate audible warning of a high signal level.

## Step by step implementation

### Project scoping

OK, let's clarify the numbers:

Input signal is (according to Hamamatsu [C9744 photon counting unit](https://www.hamamatsu.com/us/en/product/optical-sensors/pmt/accessory-for-pmt/photon-counting-unit/C9744.html), which is actually preamplifier-discriminator (shame, Hamamatsu, shame!)):

- 5V TTL
- single pulse width 10 ns
- max pulse repetition (linear range): 4·10<sup>6</sup> pulses per second

There are no restrictions from the side of photomultiplier which are below those from preamplifier-discriminator, so these are my constraints.

### The device design

First idea was to get a fast Arduino to count pulses and it was good since it is relatively simple in realization and cheap enough for the device to get born. Let's go bold and get the fastest - Teensy 4.0. And what's more, [frequency counter is already implemented](https://www.pjrc.com/teensy/td_libs_FreqCount.html).

Teensy 4.0 have 3.3V design and 5V pulses are too high for it to be tolerated, so a level shifter is necessary. I've been advised to use [74LVC2G17](https://www.ti.com/product/SN74LVC2G17) for that purpose.

To let the device emit sound a common 5V buzzer is used, powered by 5V from USB line and drived by low switching voltage [IRLB3034 n-channel MOSFET](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/irlb3034/)

It is possible to use a buzzer to report how high the signal is by using the length of the tone: short sound - we are close to overload, long continuous tone - overload. For this purpose I have to set two thresholds - the lower and the higher ones. The device checks the signal level every 2,6 second, which is our period of he signal. If the signal is less than the lower threshold the device remains silent. If the signal is between the thresholds - the length of the tone is proportional to the distance between the lower threshold and the signal level. If the signal is larger than the higher threshold - the tone length is the longest, almost the length of the period. Though practically two-threshold signal does not add a lot to device's usability (just the sound itself is enough to warn of a high signal), it is not a hard task to code. Since this is not a commercial project I can add a redundant feature just for fun.

The final circuit:

<img src="https://github.com/serhiykobyakov/nanosecond-pulse-counter-using-Teensy/blob/main/circuit.png" alt="The circuit" width="600"/>

The device assembled (sorry for poor aesthetic, I'm not an electronics engineer...):

<img src="https://github.com/serhiykobyakov/nanosecond-pulse-counter-using-Teensy/blob/main/counter_photo.jpg" width="800"/>


