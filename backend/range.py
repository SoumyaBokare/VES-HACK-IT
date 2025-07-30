import pandas as pd

# Load the dataset
file_path = "Crop_recommendation.csv"  # Update with the correct path if needed
crop_data = pd.read_csv(file_path)

# Get the range (min, max) of each feature for each crop type
crop_ranges = crop_data.groupby("label").agg(["min", "max"])

# Display the result
print(crop_ranges)

# Save the output as a CSV file
crop_ranges.to_csv("crop_parameter_ranges.csv")

# Optional: If you want to save it as an Excel file
# crop_ranges.to_excel("crop_parameter_ranges.xlsx")
