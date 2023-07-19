int received_tail = 0x00;
int pin[10] = {3, 4, 5, 6, 7, 8, 9, 12, 10, 11};
int rxbuffer[10] = {0, 0, 0, 0, 0, 0, 0, 0};
int txbuffer[3] = {0, 0, 0};
const int debounceDelay = 50; // 防抖延迟时间，单位为毫秒
int state = 0;
int mode = 1;
int taskStatus = 0;
 void setup() {
  Serial.begin(38400);
  for (int i = 0; i < 8; i++) {
    pinMode(pin[i], INPUT);
  }
  for (int i = 8; i < 10; i++) {
    pinMode(pin[i], OUTPUT);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
  }
}

 void loop() {
  checkButtonPresses();
   while (Serial.available()) {
    if (Serial.read() == 0xAA) {
      for (int i = 0; i < 10; i++) {
        while (!Serial.available());
        rxbuffer[i] = (int)Serial.read();
      }
      while (!Serial.available());
      received_tail = Serial.read();
      if (received_tail == 0xFF) {
        // 处理接收到的数据
      }
    }
  }
   ssend();
}

unsigned long lastDebounceTime[3] = {0, 0, 0}; // 上次按键状态改变的时间
 void checkButtonPresses() {
  if (digitalRead(pin[0]) == HIGH) {
    if (millis() - lastDebounceTime[0] >= debounceDelay) {
      incrementMode();
    }
    lastDebounceTime[0] = millis();
  }
  if (digitalRead(pin[1]) == HIGH) {
    if (millis() - lastDebounceTime[1] >= debounceDelay) {
      readBinaryNumber();
    }
    lastDebounceTime[1] = millis();
  }
  if (digitalRead(pin[2]) == HIGH) {
    if (millis() - lastDebounceTime[2] >= debounceDelay) {
      setTaskStatus();
    }
    lastDebounceTime[2] = millis();
  } 
}


 void incrementMode() {
  mode++;
  if (mode > 3) {
    mode = 1;
  }
}
void readBinaryNumber() {
  char binaryNumber = 0;
  for (int i = 3; i <= 6; i++) {
    binaryNumber = (binaryNumber << 1)+digitalRead(pin[i]);
  } // 将二进制转换为十六进制
  txbuffer[1] = txbuffer[2];
  txbuffer[2] = binaryNumber;
}

 void setTaskStatus() {
   taskStatus = !taskStatus;
  txbuffer[0] = taskStatus;
}
 void ssend() {
  if (state == 0) {
    Serial.write(0xAA);
    state = 1;
  } else if (state == 1) {
    Serial.write(txbuffer[0]);
    state = 2;
  } else if (state == 2) {
    Serial.write(txbuffer[1]);
    state = 3;
  } else if (state == 3) {
    Serial.write(txbuffer[2]);
    state = 4;
  } else if (state == 4) {
    Serial.write(mode);
    state = 5;
  } else if (state == 5) {
    Serial.write(0xFF);
    state = 0;
  }
}
