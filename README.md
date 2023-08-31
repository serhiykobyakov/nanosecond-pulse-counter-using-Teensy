# Short pulse counter for photon counting using Teensy 4.0

## Goal
There is a need for short TTL pulses counter with the following requirements:
* input: 5V, 10ns wide square pulses, there are already established signal line using BNC cables with 50 Ohm input on the receiver side
* counter must be able to count pulses in measuring intervals from 0.05 to 4 seconds
* counter must release warning sound when measuring signal exceed certain allowed value
* communication with PC via USB port

![Alt Text](https://github.com/serhiykobyakov/nanosecond-pulse-counter-using-Teensy/blob/main/circuit.png)
