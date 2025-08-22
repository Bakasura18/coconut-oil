# coconut-oil
Repository containing my files for Team Janus Inductions 2025, Avionics Subsystem, Round 1. 

TINKERCAD LINK TO TASK 2
https://www.tinkercad.com/things/8hEK5pSIU8q-janustask2?sharecode=5iYkRdg6f6MT1YnKZ3OKS6KyU_17Ls0yXgMK23bvd6U





TASK 1
This Task was quite hard for me. I was not at all familiar with the matplotlib and pandas. I watched a lot of YouTube videos, went back and forth with ChatGPT and finally began to understand things and could write some code on my own. First, I stored the values from the .csv file to 'data'. Next I converted it to numeric by using pd.to_numeric() and.dropna() to drop stuff which can't be converted to numeric. To convert the pressure data to altitude, I used the standard barometric formula:
h = 44330 * (1 - (P/P0)^(0.19026))
Since the test was done in the lower troposphere with not much changes in temperature and value of g, we can safely use this result. 
Used rolling mean by taking average of 2 values o adjacent side to smoothen out data fluctuations. Found out velocities using difference of 2 consecutive smoothened altitude readings. Next defined 2 axes one for velocity and one for altitude with the x axis as time. Next, used the init(), update(frame) and FuncAnimation to plot a new frame every second. 





TASK 2
I was already familiar with Arduino. So, I could easily wire up the force sensor, LEDs and the buzzer. Although I could refer some websites to find out the LED series resistor, I just assumed a 10mA limit for all and got R=5V/10mA = 500ohms. I had already worked on the force sensor for the ArchAngel Induction Task, so I used my experience from that.

I thought a lot over the algorithm for ascending/descending/apogee detection and to decide how to smoothen out the data. Discussed it with my friends in the mess too. Finally, I came up with this 
**logic:**
{
So, in my program, I read the sensor value every 50ms and take the average of 10 readings. 10 is a lot of readings, so this smoothens out any fluctuations in the data. Now, I get a an average value every half second. Also, analogRead() value is monotonous to force and pressure which are monotonous to altitude.(force to altitude is a monotonous mapping). So, there is no need to calculate the pressure or the altitudes.
Next, I created an array with 2 positions. The second position to store the latest average and the first position to store the previous average. 

Note: I have used analogRead() as a proxy for force as they are a monotonously increasing mapping.
Its ascending if the new average force < the old average force    
Its descending if the new average force > the old average force
At the first time when new average force> old average force its at apogee and a switch is turned on so that apogee condition is not triggered again
}


  
