import json

import matplotlib.pyplot as plt
import pandas as pd

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

with open('diagnostics.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data['spindle_data_stack'])

# Convert Unix timestamp to datetime
df['time'] = pd.to_datetime(df['time'], unit='s')

df = pd.concat([df.drop(['spindle'], axis=1), df['spindle'].apply(pd.Series)], axis=1)

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

load, = ax1.plot(df['time'], df['load'], label='Spindle Load')
voltage, = ax1.plot(df['time'], df['voltage'], label='Spindle Voltage')
temp, = ax1.plot(df['time'], df['temperature'], label='Spindle Temperature')
killtime, = ax1.plot(df['time'], df['kill_time'], label='Spindle Killtime')
speed, = ax2.plot(df['time'], df['speed'], label='Spindle Speed', color='black')
lines = [load, voltage, temp, killtime, speed]

if data["spindle_free_load"]:
    free_load, = ax1.axhline(y=data['spindle_free_load'], color='r', linestyle='--', label='Spindle Free Load')
    lines.append(free_load)

plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Spindle Parameters Over Time')
labels = [l.get_label() for l in lines]
plt.legend(lines, labels, loc='upper right')
plt.grid(True)
plt.show()
