/*
 * Copyright Filip Kosel 2023
 *
 * This code is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

/* CUSTOM SKETCH TO ONLY PULL tVOC DATA FROM ARDUINO, NO CO2 */

/*
 * Note: Comments are surrounded by '/* ... */'
 * Code preceeded by '//' are functional lines of code that can be used as needed
 */



#include "CCS811.h"


/*
 * Set sensor address.
 * IIC address default 0x5A, the address becomes 0x5B if the ADDR_SEL pad is soldered.
 */
CCS811 sensorA(&Wire, /*IIC_ADDRESS=*/0x5A);
CCS811 sensorB(&Wire, /*IIC_ADDRESS=*/0x5B);

/*
 * Create variables for time counters
 * Used for matching tVOC readings with time of experiment
 * Can also be used to tweak delays to get code to run closer to sensor reading times
 */
unsigned long runtime1 = 0;
unsigned long runtime2 = 0;
unsigned long runtime3 = 0;

/* Create variables to run/trigger the experiment */
//int runExp = 0; /* Used to trigger experiment start/stop based on external input */
//int triggerPinInput = 12; /* Set input pin for external start/stop trigger */

/* Create tVOC baseline variables */
int sensorAbaseline = 0;
int sensorBbaseline = 0;



/* Initialize Arduino */
void setup() {
  
    Serial.begin(115200); /* Set serial communication */
    
    /* Wait for the chip to be initialized completely, and then exit */
    while(sensorA.begin() != 0){
        Serial.println("failed to initialize Sensor A, please check chip connection.");
        delay(1000);
    }

    while(sensorB.begin() != 0){
        Serial.println("failed to initialize Sensor B, please check chip connection.");
        delay(1000);
    }

   
    /* Set measurement cycle length (250 msec) */
    sensorA.setMeasCycle(sensorA.eCycle_250ms);
    sensorB.setMeasCycle(sensorB.eCycle_250ms);


    /* Use following lines for starting experiment using external trigger */
    // pinMode(triggerPinInput, INPUT);

    //while(runExp == 0) {
    //  runExp = digitalRead(triggerPinInput);
    //  Serial.println(runExp);
    //}


    /* Delay in msec before starting experiment for sensor to warm up */
    delay(5000);


    /* Use to set single baseline during setup instead of checking each cycle */
    //sensorAbaseline = sensorA.readBaseLine();
    //sensorBbaseline = sensorB.readBaseLine();


    /* Set runtimes to 0 before starting readings */
    runtime1 = 0;
    runtime2 = 0;
    runtime3 = 0;


    /* Set analogue ground reference to external if needed for pin input */
    //analogReference(EXTERNAL);
}



/* Main loop to read VOC levels */
void loop() {
  
    /* Check runtime at the start of the loop */
    runtime1 = millis();

    
    /* Following lines can be used for debugging/testing */
    //sensorA.writeBaseLine(0); // SET BASELINE TO 0 FOR TESTING
    //sensorB.writeBaseLine(0); // SET BASELINE TO 0 FOR TESTING
    
    //sensorA.writeBaseLine(sensorAbaseline); // SET BASELINE FROM READINGS
    //sensorB.writeBaseLine(sensorBbaseline); // SET BASELINE FROM READINGS


    /* Check if SensorA is ready
     * If SensorA ready, print baseline and tVOC readings
     * If SensorA not ready, print 'NA' for baseline and tVOC readings
     */
    if(sensorA.checkDataReady() == true){
      
        Serial.print("A_base_");
        Serial.println(sensorA.readBaseLine());
        Serial.print("A_tVOC_");
        Serial.println(sensorA.getTVOCPPB());
        
    } else {
      
        Serial.println("A_base_NA");
        Serial.println("A_tVOC_NA");
        
    }


    /* As above, but for SensorB */
    if(sensorB.checkDataReady() == true){
      
        Serial.print("B_base_");
        Serial.println(sensorB.readBaseLine());
        Serial.print("B_tVOC_");
        Serial.println(sensorB.getTVOCPPB());
        
    } else {
      
        Serial.println("B_base_NA");
        Serial.println("B_tVOC_NA");
        
    }


    /* Check runtime after sensor readings */
    runtime2 = millis();


    /*
     * Check input pins to identify which valves are being triggered and print output
     * Note: these should use variables set up at the top
     */
    if(digitalRead(8) == 1) {
      Serial.println("stim_1");
    } else if(digitalRead(9) == 1) {
      Serial.println("stim_2");
    } else if(digitalRead(10) == 1) {
      Serial.println("stim_3");
    } else if(digitalRead(11) == 1) {
      Serial.println("stim_4");
    } else {
      Serial.println("stim_0");
    }


    /* Check runtime after checking valve triggers */
    runtime3 = millis();


    /* Print all three runtime readings */
    Serial.print("msec1_");
    Serial.println(runtime1);
    Serial.print("msec2_");
    Serial.println(runtime2);
    Serial.print("msec3_");
    Serial.println(runtime3);

    /*
     * 250 msec delay before next sensor reading
     * This can be adjusted based on runtime readings to make code run closer to the timing of sensor readings
     */
    delay(250);
}
