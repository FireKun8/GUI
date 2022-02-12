#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <MPU6050.h>
#include <I2Cdev.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp280;
const int mpuAddress = 0x68;
MPU6050 mpu(mpuAddress);

int16_t ax, ay, az;
int16_t gx, gy, gz;
float inPres;

const float accScale = 2.0 * 9.81 / 32768.0;
const float gyroScale = 250.0 / 32768.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  if(!bmp280.begin()){
    Serial.println("BMP280 not detected!");
    while(1);
  }
  if(!mpu.testConnection()){
    Serial.println("MPU6050 not detected!");
    while(1);
  }
  inPres = bmp280.readPressure();
}

void loop() {
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  float altitude = bmp280.readAltitude(inPres / 100);

  Serial.print(altitude);
  Serial.print("/");
  Serial.print(ax * accScale);
  Serial.print("/");
  Serial.print(ay * accScale);
  Serial.print("/");
  Serial.print(az * accScale);
  Serial.print("/");
  Serial.print(gx * gyroScale);
  Serial.print("/");
  Serial.print(gy * gyroScale);
  Serial.print("/");
  Serial.print(gz * gyroScale);
  Serial.println();

  delay(200);
}