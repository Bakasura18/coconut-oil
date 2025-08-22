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
x = range(len(altitudes))  # creates a sequence of 0,1,2,3.. till length of altitudes-1

# --- Animation Setup ---
fig, ax1 = plt.subplots()

# defining a y axis - Altitude axis
ax1.set_xlim(0, len(altitudes))
ax1.set_ylim(min(altitudes.min(), altitudes_smooth.min()) - 5,
             max(altitudes.max(), altitudes_smooth.max()) + 5)

raw_line, = ax1.plot([], [], 'bo-', markersize=2, alpha=0.5, label="Raw Altitude")
smooth_line, = ax1.plot([], [], 'ro-', markersize=2, label="Smoothed Altitude")

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Altitude (m)", color='black')
ax1.grid(True)

# defining another y axis - Velocity axis 
ax2 = ax1.twinx()
ax2.set_ylim(velocities.min() - 1, velocities.max() + 1)
vel_line, = ax2.plot([], [], 'g--', linewidth=1.5, label="Vertical Velocity (m/s)")  # velocity line in green dashed
ax2.set_ylabel("Velocity (m/s)", color='green')


lines = [raw_line, smooth_line, vel_line]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left", frameon=True)

# function to initialise
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

# 1 frame = 1 second
ani = animation.FuncAnimation(fig, update, frames=len(altitudes),
                              init_func=init, blit=True, interval=1000, repeat=False)

plt.show()
