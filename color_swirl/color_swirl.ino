// color swirl! connect an RGB LED to the PWM pins as indicated
// in the #defines
// public domain, enjoy!

#define REDPIN 5
#define GREENPIN 6
#define BLUEPIN 3

#define FADESPEED 2     // make this higher to slow down

int r, g, b;

int incomingByte = 0;
bool receivingColor = false;
int RGBReceiving = 0;
String RGBReceived[] = {"", "", ""};
int RGBConverted[] = {0, 0, 0};

void setup() {
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);
  Serial.begin(57600);
  r = 255;
  g = 255;
  b = 255;
}


void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    //Serial.print("I received: ");
    //Serial.println(incomingByte, DEC);
    if (incomingByte == 10) {
    } else if (incomingByte == 40) {
      receivingColor = true;
    } else if (incomingByte == 41) {
      receivingColor = false;
      RGBReceiving = 0;

      RGBConverted[0] = RGBReceived[0].toInt();
      RGBConverted[1] = RGBReceived[1].toInt();
      RGBConverted[2] = RGBReceived[2].toInt();
      RGBReceived[0] = "";
      RGBReceived[1] = "";
      RGBReceived[2] = "";

      r = min(max(RGBConverted[0], 0), 255);
      g = min(max(RGBConverted[1], 0), 255);
      b = min(max(RGBConverted[2], 0), 255);
      //Serial.println("(" + String(RGBConverted[0]) + ", " + String(RGBConverted[1]) + ", " + String(RGBConverted[2]) + ")");
      //Serial.println("r:" + String(r) + ", g:" + String(g) + ", b:" + String(b));
    } else if (incomingByte == 44) {
      RGBReceiving = RGBReceiving + 1;
      //Serial.println("incremented " + String(RGBReceiving));
    } else if (incomingByte >= 48 && incomingByte <= 57) {
      RGBReceived[RGBReceiving] = RGBReceived[RGBReceiving] + String(incomingByte - 48);
    }
  }

  analogWrite(REDPIN, r);
  analogWrite(GREENPIN, g);
  analogWrite(BLUEPIN, b);
}
