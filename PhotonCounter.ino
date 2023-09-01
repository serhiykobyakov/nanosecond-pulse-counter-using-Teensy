//
// Short pulse counter for photon counting using Teensy 4.0
//
// (c) Serhiy Kobyakov
// version 2023-09-01
//
// info page: https://www.pjrc.com/teensy/td_libs_FreqCount.html
// newest source files found: https://github.com/PaulStoffregen/FreqCount
//


#include <arm_math.h>
#include <FreqCount.h>

#if defined(__IMXRT1062__)
extern "C" uint32_t set_arm_clock(uint32_t frequency);
#endif


// Board connections:
#define BuzzerPin 14
#define FreqInputPin 9


unsigned long last_cps_read;   // timestamp for last signal reading
unsigned long signal_check_interval_ms = 2600; // interval for idle sinal checking in ms
double max_pm_cps = 1000000.0; // max cps after which the photomultiplier exceeds it's linear range
double max_cps = 4000000.0;    // max cps after which the preamplifier-discriminator exceeds it's linear range

double meas_interval = 0.4;       // variable for default measuring interval value
//double a0 = 0.000001676145;
//double a1 = 1.000016;

unsigned long counts = 0;      // variable for pulses read
double cps = 0.0;              // variable for the final result: counts per second


void beepn(int times) {
// make n beeps using buzzer

  for (int i = 0; i < times; i++) {
    digitalWrite(BuzzerPin, HIGH);
    delay(60);
    digitalWrite(BuzzerPin, LOW);
    delay(60);
  }
}


unsigned long getGateInterval(float expose) {
// calculate value of measurement gate length
// in microseconds (for Teensy 4.0)
// for actual measuring interval

//  return (unsigned long) (1000000) * expose / a1 - (1000000) * a0;
  return (unsigned long) (1000000L * expose);
}


void set_meas_interval(double newexp) {
// set default measuring interval value in seconds
// for further readings

  if (newexp <= 0.05) meas_interval = (double) 0.05;
  else if ((newexp > 0.05) && (newexp <= 4.0)) meas_interval = (double) newexp;
  else meas_interval = (double) 4.0;
}


double get_cps(float expo) {
// get cps value from device (counts per second)
  
  FreqCount.begin(getGateInterval(expo));
  counts = 0;
  while (counts <= 0.0) {
    if (FreqCount.available()) {
      counts = FreqCount.read();
      cps = (double) counts / expo;
    }
  }
  FreqCount.end();
  last_cps_read = millis();

// make warning sound if the signal is higher than max_cps value
  unsigned int signal_duration = 0;
  if (cps < max_pm_cps) signal_duration = 0;
  else if ((cps >= max_pm_cps) && (cps < max_cps)) signal_duration = (unsigned int) (signal_check_interval_ms - 100) * (cps - max_pm_cps) / max_cps + 100;
  else signal_duration = signal_check_interval_ms;

  if (signal_duration > 0) {
    digitalWrite(BuzzerPin, HIGH);
    delay(signal_duration);
    digitalWrite(BuzzerPin, LOW);
  }

  return cps;
}


unsigned long get_counts(float expo) {
// read cps from device (counts per second)
// can be removed after testing and calibration
  
  FreqCount.begin(getGateInterval(expo));
  counts = 0;
  while (counts <= 0.0) {
    if (FreqCount.available()) {
      counts = FreqCount.read();
    }
  }
  FreqCount.end();

  last_cps_read = millis();
  return counts;
}


int get_prn_prec() {
// get the output precision of cps result
// depending on measuring interval value
  
  int prec;
  if (meas_interval <= 1.0) prec = 0;
  else prec = 1;

  return prec;
}


void setup() {
// make short sound on setup start
  digitalWrite(BuzzerPin, HIGH);
  delay(50);
  digitalWrite(BuzzerPin, LOW);
  
// start serial communication
  Serial.begin(115200);
  while (!Serial);  // wait until serial monitor is ready

#if defined(__IMXRT1062__)
  set_arm_clock(400000000); // set 400 MHz
//  Serial.print("F_CPU_ACTUAL=");
//  Serial.println(F_CPU_ACTUAL);
#endif

  last_cps_read = millis();
}


void loop() {
// MAIN LOOP

  if (Serial.available()) {
    int char_in = Serial.read();
    switch (char_in) {
      case '?':  // identification
          delay(4);
          Serial.println("PhotonCounter");
          break;
      
      case 'z':  // make some sound
          beepn(5);
          break;

      case 'r':  // make reading and send it via Serial
            Serial.println(get_cps(meas_interval), get_prn_prec());
          break;

      case 'R':  // make 500 readings and send it via Serial
                 // for testing purpouses only, will be removed later
          unsigned int counter = 0;
          while (counter <= 500) {
            Serial.println(get_cps(meas_interval), get_prn_prec());
//            Serial.println(get_counts(meas_interval));
            delay(300);
            counter++;
          }
          break;

      case 'e':  // set default measuring interval
          delay(5);
          if (Serial.available()) {
            String newstr = Serial.readString();
            double newexp = newstr.trim().toFloat();
            if (newexp != 0.0) set_meas_interval(newexp);
            else {
              beepn(3);
//              Serial.print("wrong value for measuring interval: ");
//              Serial.println(newstr);
            }
          }
          Serial.println(meas_interval);
          break;

      case '\n':
          break;
    }
  }


// check signal level to detect overload
// when idle
  if (millis() > last_cps_read + signal_check_interval_ms) get_cps(0.1);
}
