import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed data
df = pd.read_csv("preprocessed_sensor_data.csv")

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Set timestamp as index for time-series visualization
df.set_index("timestamp", inplace=True)

# Plot sensor values over time
plt.figure(figsize=(12, 6))
df[["humidity", "temperature", "soil_sensor_1", "soil_sensor_2"]].plot(figsize=(12, 6))
plt.title("Sensor Readings Over Time")
plt.xlabel("Time")
plt.ylabel("Normalized Values")
plt.legend(loc="upper right")
plt.grid()
plt.show()

# Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Between Sensor Readings")
plt.show()

# Distribution of sensor values
df[["humidity", "temperature", "soil_sensor_1", "soil_sensor_2"]].hist(figsize=(12, 6), bins=30)
plt.suptitle("Distribution of Sensor Readings")
plt.show()
