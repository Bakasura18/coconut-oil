// C++ code
//
int red = 11;  //as red is connected to digitalpin 11
int yellow=13;
int green=12;

float arr[10];
int counter=0;
float state;

float sensor,force;
float k=1.0/40142; //I determined it experimentally
float f_avg=0;

int counter1=0; 
int descentswitch=0;//switch which triggers only once at apogee
int j=0;
float sum=0;

//creating an array of size 2 with avg[1] to store the average value
//of 10 readings over the past half second and avg[0] to store the 
//average of the past -1  to -0.5 second
float avg[2] = {0.0, 0.0}; 


void setup()
{
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(A0,INPUT);
  pinMode(10,OUTPUT);
  digitalWrite(yellow,LOW); //just ensuring the LEDs are off
  digitalWrite(green,LOW);
 
}

void loop()
{
  sum = 0;
  for (int i=0;i<10;i++) //loop to find average of 10 readings over past half second
  {sum+=analogRead(A0);  //to smoothen out the fluctuations
  delay(50);
  }
  avg[0]=avg[1];
  avg[1]=sum/10.0;
  j++;
  
  if(avg[0]>avg[1]+5 && j>1) // ascending condition
  {digitalWrite(red,HIGH);
digitalWrite(green,LOW);}
  
  if(descentswitch==0 && avg[1] >avg[0]+5 && j>1)//apogee condition
  {descentswitch++;
   digitalWrite(green,HIGH);
   digitalWrite(yellow,HIGH);
   digitalWrite(10,HIGH);
   delay(1000);
  digitalWrite(10,LOW);
  digitalWrite(yellow,LOW);}
  
  if (avg[1]>avg[0]+5 && j>1) //descending condition
  {digitalWrite(red,LOW);
  digitalWrite(green,HIGH);};
  
}
  
  
  
  
 
   
  

    

 


