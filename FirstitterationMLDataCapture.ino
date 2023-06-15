#include <Wire.h>

const int I2C_address_MPU = 0x68;
const int LSB_per_g = 8192; // LSB per g for ±4g sensitivity range

int16_t accel_x, accel_y, accel_z;
int16_t gyro_x, gyro_y, gyro_z;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(I2C_address_MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}

void loop() {
  Wire.beginTransmission(I2C_address_MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(I2C_address_MPU, 14, true);

  accel_x = Wire.read() << 8 | Wire.read();
  accel_y = Wire.read() << 8 | Wire.read();
  accel_z = Wire.read() << 8 | Wire.read();
  Wire.read(); // Discard temperature high byte
  Wire.read(); // Discard temperature low byte
  gyro_x = Wire.read() << 8 | Wire.read();
  gyro_y = Wire.read() << 8 | Wire.read();
  gyro_z = Wire.read() << 8 | Wire.read();

  // Convert accelerometer readings to actual acceleration values in g
  float acceleration_x = accel_x / (float)LSB_per_g;
  float acceleration_y = accel_y / (float)LSB_per_g;
  float acceleration_z = accel_z / (float)LSB_per_g;

  Serial.print("accel_x: "); Serial.print(acceleration_x);
  Serial.print(", accel_y: "); Serial.print(acceleration_y);
  Serial.print(", accel_z: "); Serial.print(acceleration_z);
  Serial.print(", gyro_x: "); Serial.print(gyro_x);
  Serial.print(", gyro_y: "); Serial.print(gyro_y);
  Serial.print(", gyro_z: "); Serial.print(gyro_z);
  Serial.println();

  delay(100);
}
