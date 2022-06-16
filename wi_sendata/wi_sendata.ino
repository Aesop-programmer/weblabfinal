#include <WiFi.h>
#include <WiFiUdp.h>
#include "MPU9250.h"
/* WiFi network name and password */
MPU9250 mpu;
const char * ssid = "Ven_peap";
const char * pwd = "";

// IP address to send UDP data to.
// it can be ip address of the server or 
// a network broadcast address
// here is broadcast address
const char * udpAddress = "192.168.139.106";
const int udpPort = 44444;
int buttonState = 0;
int diffbutton = 0;

int loop_cnt=0;
//create UDP instance
WiFiUDP udp;

uint8_t buffer[1500] = "";
char buf3[1500]="";
char buf2[60]="";

void setup(){
   //Connect to the WiFi network
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.begin(19200);
  Wire.begin();
  delay(2000);

    if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
    }
//    Serial.println("Accel Gyro calibration will start in 5sec.");
//    Serial.println("Please leave the device still on the flat plane.");
    mpu.verbose(true);
    delay(5000);
    mpu.calibrateAccelGyro();

//    Serial.println("Mag calibration will start in 5sec.");
//    Serial.println("Please Wave device in a figure eight until done.");
//    delay(5000);
//    mpu.calibrateMag();
//  
//    print_calibration();
//    mpu.verbose(false);
    mpu.setFilterIterations(15);
    pinMode(25,INPUT_PULLUP);
    int i = 0;
    uint8_t buffer[1500] = "";
    char buf3[1500]="";
    char buf2 [60]="";
     int cnt_len=0;
    while(i < 50 ){
       if (mpu.update()) {
       static uint32_t prev_ms = millis();
       if (millis() > prev_ms + 1) {
//          sprintf(buf2,"%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",mpu.getGyroX(),mpu.getGyroY(),mpu.getGyroZ(),mpu.getAccX(),mpu.getAccY(),mpu.getAccZ(),mpu.getMagX(),mpu.getMagY(),mpu.getMagZ());
            sprintf(buf2,"%.2f,%.2f,%.2f\n",mpu.getAccX(),mpu.getAccY(),mpu.getAccZ());
//            Serial.print("buf2");
            delay(50);
          cnt_len+=strlen(buf2);
//          Serial.println(strlen(buf2));
          Serial.println("show buf2");
          Serial.println(buf2);
          strncat(buf3,buf2,strlen(buf2));
          memset(buf2,0,60);

           prev_ms = millis();
           i = i +1;
           Serial.printf("i is \n");
           Serial.print(i);
           Serial.printf("\n");
       }
       }
       
      }
      Serial.println("stage2....");
      memcpy(buffer,buf3,cnt_len);
      for(int t=0;t<1;t++){
      udp.beginPacket(udpAddress, udpPort);
      udp.write(buffer,cnt_len-1);
      udp.endPacket();
      }
  memset(buffer,0,1500);
  memset(buf3,0,1500);
  memset(buf2,0,60);
  
 Serial.println("stage2....");
}

void loop(){
  Serial.printf("loop cnt is ");
  Serial.println(loop_cnt);
   
  buttonState = digitalRead(25);
  if(buttonState != diffbutton){
    int i = 0;
   
    int my_len=0;
    while(i < 50){
      if (mpu.update()) {
          
          //This initializes udp and transfer buffer
//          sprintf(buf2,"%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",mpu.getGyroX(),mpu.getGyroY(),mpu.getGyroZ(),mpu.getAccX(),mpu.getAccY(),mpu.getAccZ(),mpu.getMagX(),mpu.getMagY(),mpu.getMagZ());
          sprintf(buf2,"%.2f,%.2f,%.2f\n",mpu.getAccX(),mpu.getAccY(),mpu.getAccZ());
//          Serial.println(strlen(buf2));
          my_len+=strlen(buf2);
          strncat(buf3,buf2,strlen(buf2));
          Serial.println("show buf2");
          Serial.println(buf2);
          memset(buf2,0,60);
           i = i +1;
          Serial.printf("i is ");
         Serial.println(i);
//          memset(buffer[i], 0, 50);
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 500) {
//         getgyro();
//         acc();
//         //linearacc();
//         Mag();
//           delay(500);
         prev_ms = millis();
         Serial.printf("i is ");
         Serial.println(i);
       
      }
   }
   
   
      }
    memcpy(buffer,buf3,my_len);
    Serial.println("my_stop point");
    for(int z=0;z<1;z++){
      udp.beginPacket(udpAddress, udpPort);
      udp.write(buffer,my_len-1);
      udp.endPacket();
    }
    memset(buffer,0,1500);
    memset(buf3,0,1500);
    memset(buf2,0,60);
    Serial.println("my_stop point");
    
   diffbutton = diffbutton^(1);
   Serial.println("my_stop point333");
    }
    else{
    Serial.println("my_stop point2");
    uint8_t buf7[5]="off\n";
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf7,4);
    udp.endPacket();
    Serial.println("off");
    
    }
    Serial.println("my_stop point444");
}



void print_roll_pitch_yaw() {
    Serial.print("Yaw, Pitch, Roll: ");
    Serial.print(mpu.getYaw(), 2);
    Serial.print(", ");
    Serial.print(mpu.getPitch(), 2);
    Serial.print(", ");
    Serial.println(mpu.getRoll(), 2);
}

void getgyro() {
  Serial.print(mpu.getGyroX(), 2);
  Serial.print(",");
  Serial.print(mpu.getGyroY(), 2);
  Serial.print(",");
  Serial.print(mpu.getGyroZ(), 2);
  Serial.print(",");
  }
void acc(){
  Serial.print(mpu.getAccX(), 2);
  Serial.print(",");
  Serial.print(mpu.getAccY(), 2);
  Serial.print(",");
  Serial.print(mpu.getAccZ(), 2);
  Serial.print(",");
  }
void Mag() {
  Serial.print(mpu.getMagX(), 2);
  Serial.print(",");
  Serial.print(mpu.getMagY(), 2);
  Serial.print(",");
  Serial.println(mpu.getMagZ(), 2);
  }
void linearacc() {
  Serial.print(mpu.getLinearAccX(),2);
  Serial.print(",");
  Serial.print(mpu.getLinearAccY(),2);
  Serial.print(",");
  Serial.print(mpu.getLinearAccZ(),2);
  Serial.print(",");
  }
void print_calibration() {
    Serial.println("< calibration parameters >");
    Serial.println("accel bias [g]: ");
    Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.println();
    Serial.println("gyro bias [deg/s]: ");
    Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.println();
    Serial.println("mag bias [mG]: ");
    Serial.print(mpu.getMagBiasX());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasY());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasZ());
    Serial.println();
    Serial.println("mag scale []: ");
    Serial.print(mpu.getMagScaleX());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleY());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleZ());
    Serial.println();
}
