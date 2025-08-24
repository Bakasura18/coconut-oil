import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

data = pd.read_csv('data.csv', header=None)  # to read the data from the csv file and store it in data
pressures = pd.to_numeric(data[0], errors='coerce').dropna()  # to convert the strings stored in first column of data to numbers and to remove stuff that cant be converted to numbers

P0 = 101325  # standard air pressure at sea level

altitudes = 44330 * (1 - (pressures / P0) ** 0.1903)  # converting pressure to altitude

# Smoothening the altitude curve using rolling mean
altitudes_smooth = altitudes.rolling(window=3, center=True).mean()  # takes mean of itself and 2 adjacent data points 
altitudes_smooth = altitudes_smooth.fillna(method="bfill").fillna(method="ffill")  # filling NaN values at edges

velocities = altitudes_smooth.diff().fillna(0)  # Calculate velocities as the difference between consecutive altitudes  
x = range(len(altitudes))  # creates a sequence of 0,1,2,3.. till length of altitudes-1 (its a range object)

# Animation part
fig, ax1 = plt.subplots()#to create 2 objects, fig for the canvas and ax1 for the axes.

# defining a y axis - Altitude axis
ax1.set_xlim(0, len(altitudes)) #setting x axis limits 
ax1.set_ylim(min(altitudes.min(), altitudes_smooth.min()) - 5,
             max(altitudes.max(), altitudes_smooth.max()) + 5) #so that graph doesnt touch the bottom, adding a margin of 5

raw_line, = ax1.plot([], [], 'bo-', markersize=2, alpha=0.5, label="Raw Altitude")#a Line2D object for raw altitudes
smooth_line, = ax1.plot([], [], 'ro-', markersize=2, label="Smoothed Altitude")#a Line2D object for smoothened altitudes

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Altitude (m)", color='black')
ax1.grid(True)#turn on  gridlines

# defining another y axis - Velocity axis 
ax2 = ax1.twinx()#to make a twin y axis that shares the same x axis.
ax2.set_ylim(velocities.min() - 1, velocities.max() + 1)#again to add some margin 
vel_line, = ax2.plot([], [], 'g--', linewidth=1.5, label="Vertical Velocity (m/s)")  # the comma is because it returns a tuple.
ax2.set_ylabel("Velocity (m/s)", color='green')


lines = [raw_line, smooth_line, vel_line]  #maing a python list to have all three line2D objects
labels = [l.get_label() for l in lines] #to gather all 3 labels into  a list
ax1.legend(lines, labels, loc="upper left", frameon=True)# to put the legend at the top left in a box

# function to initialise - to execute before the first frame (can be omitted though i.e. its optional)
def init(): 
    raw_line.set_data([], [])
    smooth_line.set_data([], [])
    vel_line.set_data([], [])
    return raw_line, smooth_line, vel_line

# function to update
def update(frame):
    raw_line.set_data(x[:frame], altitudes[:frame])
    smooth_line.set_data(x[:frame], altitudes_smooth[:frame])
    vel_line.set_data(x[:frame], velocities[:frame])
    return raw_line, smooth_line, vel_line



ani = animation.FuncAnimation(fig, update, frames=len(altitudes),
                              init_func=init, blit=True, interval=1000, repeat=False)
#calls the function update at each frame,
#frames=len(altitudes) : this passes values from [0,1,2,3...len(altitudes)] to the update function, i.e. the source of data to pass to the update function with each frame
#init_func=init : to execute before the first frame. 
# blit=True : to turn on blitting so that only the part that changed is updated with each frame and not the whole stuff
#interval=1000 : to display each new frame after 1000 milli seconds
#repeat=False : to not repeat the animation after its over.
plt.show()

