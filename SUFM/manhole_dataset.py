import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
num_samples = 1000

# Generate random data for manhole sensors
data = {
    "debris_level": np.random.randint(10, 150, num_samples),         # Debris level in kg
    "water_level": np.random.randint(10, 300, num_samples),          # Water level in cm
    "methane_ppm": np.random.randint(5, 150, num_samples),           # Methane gas in ppm
    "h2s_ppm": np.random.randint(1, 80, num_samples),                # Hydrogen sulfide gas in ppm
    "co_ppm": np.random.randint(1, 100, num_samples),                # Carbon monoxide in ppm
}

# Flood status based on water and gas levels
def generate_flood_status(row):
    # Flood conditions
    if (
        row['water_level'] > 200 or
        row['debris_level'] > 100 or
        row['methane_ppm'] > 100 or
        row['h2s_ppm'] > 50 or
        row['co_ppm'] > 70
    ):
        return 1  # Flood risk
    else:
        return 0  # No flood

# Create DataFrame
df = pd.DataFrame(data)

# Apply flood status
df['flood_status'] = df.apply(generate_flood_status, axis=1)

# Save dataset to CSV
output_file = "manhole_flood_dataset.csv"
df.to_csv(output_file, index=False)

print(f"✅ Dataset saved as '{output_file}' with {num_samples} samples.")
