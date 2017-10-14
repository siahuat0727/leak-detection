int mic=A0;
int micout;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  micout=analogRead(mic);
  Serial.println(micout);
}
