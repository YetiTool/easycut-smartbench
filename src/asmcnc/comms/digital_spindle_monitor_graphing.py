import json

import matplotlib.pyplot as plt
import pandas as pd

with open('diagnostics.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data['spindle_data_stack'])

# Convert Unix timestamp to datetime
df['time'] = pd.to_datetime(df['time'], unit='s')

df = pd.concat([df.drop(['spindle'], axis=1), df['spindle'].apply(pd.Series)], axis=1)

plt.figure(figsize=(12, 8))

plt.plot(df['time'], df['load'], label='Spindle Load')
plt.plot(df['time'], df['voltage'], label='Spindle Voltage')
plt.plot(df['time'], df['temperature'], label='Spindle Temperature')
plt.plot(df['time'], df['kill_time'], label='Spindle Killtime')
plt.plot(df['time'], df['speed'], label='Spindle Speed')

if data["spindle_free_load"]:
    plt.axhline(y=data['spindle_free_load'], color='r', linestyle='--', label='Spindle Free Load')

plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Spindle Parameters Over Time')
plt.legend()
plt.grid(True)
plt.show()
