#include "CCS811.h"

/*
 * IIC address default 0x5A, the address becomes 0x5B if the ADDR_SEL is soldered.
 */
CCS811 sensorA(&Wire, /*IIC_ADDRESS=*/0x5A);
CCS811 sensorB(&Wire, /*IIC_ADDRESS=*/0x5B);

void setup(void)
{
    Serial.begin(115200);
    /*Wait for the chip to be initialized completely, and then exit*/
    while(sensorA.begin() != 0){
        Serial.println("failed to initialize Sensor A, please check chip connection.");
        delay(1000);
    }

    while(sensorB.begin() != 0){
        Serial.println("failed to initialize Sensor B, please check chip connection.");
        delay(1000);
    }

    sensorA.setMeasCycle(sensorA.eCycle_250ms);
    sensorB.setMeasCycle(sensorB.eCycle_250ms);

    //Serial.println("End setup section");
}


void loop() {
    if(sensorA.checkDataReady() == true){
        /*!
         * @brief Set baseline
         * @return baseline in clear air
         */
        Serial.print("Sensor A baseline: ");
        Serial.println(sensorA.readBaseLine());

        //sensorA.writeBaseLine(0x1000); // SET BASELINE TO 0 FOR TESTING

        //Serial.print("Sensor A baseline 2: ");
        //Serial.println(sensorA.readBaseLine());

        Serial.print("tVOCA: ");
        Serial.println(sensorA.getTVOCPPB());

    } else {
        Serial.println("SensorA data is not ready!");
    }
      if(sensorB.checkDataReady() == true){
        /*!
         * @brief Set baseline
         * @return baseline in clear air
         */

        //Serial.println(sensorB.getMeasurementMode());
         
        Serial.print("Sensor B baseline: ");
        Serial.println(sensorB.readBaseLine());

        //sensorB.writeBaseLine(0x1000); // SET BASELINE TO 0 FOR TESTING

        //Serial.print("Sensor B baseline 2: ");
        //Serial.println(sensorB.readBaseLine());
        
        Serial.print("tVOCB: ");
        Serial.println(sensorB.getTVOCPPB());

    } else {
        Serial.println("SensorB data is not ready!");
    }
    //delay cannot be less than measurement cycle
    delay(250);
}
