/*unsigned long time;
unsigned long endtime;
int mic=A0;
int micout;
void setup(){
  Serial.begin(57600);
  for(int i=0;i<1000;i++)
  {
    micout=analogRead(mic);
  }
   analogReference(EXTERNAL);
}
void loop(){
  time = millis();
  //prints time since program started
    for(int i=0;i<1000;i++)
  {
    micout=analogRead(mic);
     Serial.print ( micout);
  }
  endtime=millis();
  unsigned long slap= endtime-time;
  Serial.println();
  Serial.print(slap);
   Serial.println();
  // wait a second so as not to send massive amounts of data
  delay(5000);
}*/const int pin = A0;
 unsigned long n =50000;  // sample 採樣 1000 次
 String a;
void setup() {
  Serial.begin(115200);
  setP16( ) ;
analogReference(EXTERNAL);

}
void loop( ) { // 
  unsigned long begt, runt, total;
  //total = 0;  // clear before sampling
  //begt = micros();
  
    total = analogRead(pin);
    Serial.write(highByte(total));
    Serial.write(lowByte(total));
    Serial.write("\n");
  
  //runt = micros() - begt;  // elapsed time
   // Serial.println(total);
  //Serial.print(String("Time per sample: ")+runt/1.0/n +"us");
  //Serial.println(String(", Frequency: ")+1000000.0/runt*n +" Hz");
  //delay(5566);
}// loop(
void setP16( ) {
  Serial.println("ADC Prescaler = 16");  // 100
  ADCSRA |=  (1 << ADPS2);   // 1
  ADCSRA &=  ~(1 << ADPS1);  // 0
  ADCSRA &=  ~(1 << ADPS0);  // 0
}
