#include <Wire.h>

#include <SparkFun_MMC5983MA_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_MMC5983MA

SFE_MMC5983MA myMag;

void setup()
{
    bool connection = 0;
    Serial.begin(115200);
    Wire.begin();

    if (myMag.begin() == false)
    {
        //Serial.println("MMC5983MA did not respond - check your wiring. Freezing.");
        connection = 0;
        while (true)
            ;
    }

    myMag.softReset();
    connection = 1;
    //Serial.println(connection);
}

void loop()
{
    unsigned int currentX = 0;
    unsigned int currentY = 0;
    unsigned int currentZ = 0;

    currentX = myMag.getMeasurementX();
    currentY = myMag.getMeasurementY();
    currentZ = myMag.getMeasurementZ();

    Serial.print(currentX);
    Serial.print("\t");
    Serial.print(currentY);
    Serial.print("\t");
    Serial.println(currentZ);

    delay(500);
}
