int R = 7;
int G = 5;
int B = 6;
int LDR = A0;
int R_val = 0, G_val = 0, B_val = 0, RGB_val = 0;

const int HANDSHAKE = 0; 
const int MEASURE_REQUEST = 1;
int inByte = 0;

void setup() {
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT); 
  pinMode(B, OUTPUT); 

  digitalWrite(R, LOW);
  digitalWrite(G, LOW);
  digitalWrite(B, LOW);

  Serial.begin(115200);
  while(!Serial){}
}

void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();

    if (inByte == HANDSHAKE){
      if (Serial.availableForWrite()) {
          for(int i=0; i<10; i++) {
            digitalWrite(R, HIGH);
            digitalWrite(G, HIGH);
            digitalWrite(B, HIGH);     
            delay(50);

            digitalWrite(R, LOW);
            digitalWrite(G, LOW);
            digitalWrite(B, LOW);
            delay(50);
          }
        
          Serial.println("Handshake message received.");
      }
    }

    // If data is requested, fetch it and write it
    else if (inByte == MEASURE_REQUEST) {
      if (Serial.availableForWrite()) {
        digitalWrite(R, HIGH);
        delay(50);
        R_val = analogRead(LDR);
        digitalWrite(R, LOW);
        
        digitalWrite(G, HIGH);
        delay(50);
        G_val = analogRead(LDR);
        digitalWrite(G, LOW);
      
        digitalWrite(B, HIGH);
        delay(50);
        B_val = analogRead(LDR);
        digitalWrite(B, LOW);
      
        digitalWrite(R, HIGH);
        digitalWrite(G, HIGH);
        digitalWrite(B, HIGH);
        delay(50);
        RGB_val = analogRead(LDR);
        digitalWrite(R, LOW);
        digitalWrite(G, LOW);
        digitalWrite(B, LOW);
      
        String outstr = String(R_val,DEC) + "," + String(G_val,DEC) + "," + String(B_val,DEC) + "," + String(RGB_val,DEC);
        Serial.println(outstr);
      } 
    }
  }
}
