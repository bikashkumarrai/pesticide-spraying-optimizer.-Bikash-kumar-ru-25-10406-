import numpy as np
import matplotlib.pyplot as plt

# 1. Simulate Drone Image Data (100x100 pixels field)
# NIR (Near-Infrared) aur Red bands generate kar rahe hain
np.random.seed(42)
rows, cols = 100, 100

# Healthy crops mein NIR high hota hai aur Red low hota hai
nir_band = np.random.uniform(0.5, 0.9, (rows, cols))
red_band = np.random.uniform(0.05, 0.15, (rows, cols))

# Ek "Infection Hotspot" simulate karte hain (jahan plant stress high hai)
# Hotspot zone mein NIR drop ho jayega aur Red badh jayega
nir_band[40:60, 40:60] -= 0.35
red_band[40:60, 40:60] += 0.2

# 2. Calculate NDVI
# Formula: NDVI = (NIR - Red) / (NIR + Red)
# Avoid division by zero using np.seterr
np.seterr(divide='ignore', invalid='ignore')
ndvi = (nir_band - red_band) / (nir_band + red_band)

# 3. Identify Infection Hotspots (Thresholding)
# Healthy vegetation ka NDVI > 0.6 hota hai. 
# Agar NDVI 0.3 se kam hai matlab wahan infection/stress hai.
threshold = 0.3
hotspot_mask = ndvi < threshold

# 4. Extract Hotspot Coordinates for Spraying Drones
# Jahan mask True (1) hai, wahan ke pixel coordinates nikalenge
hotspot_coords = np.argwhere(hotspot_mask)

print(f"--- Project Analysis Report ---")
print(f"Total Field Pixels: {rows * cols}")
print(f"Infected Pixels Detected: {np.sum(hotspot_mask)}")
print(f"Chemical Reduction: {100 - (np.sum(hotspot_mask) / (rows * cols) * 100):.2f}% area saved from unnecessary spray!")
print(f"Sample Spray Coordinates (First 5): \n{hotspot_coords[:5]}\n")

# 5. Visualization (Result Display)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: NDVI Map
im1 = axes[0].imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
axes[0].set_title("NDVI Map (Green = Healthy, Red = Stressed)")
fig.colorbar(im1, ax=axes[0], label='NDVI Index')

# Plot 2: Spot Spraying Map (Prescription Map)
im2 = axes[1].imshow(hotspot_mask, cmap='gray_r')
axes[1].set_title("Prescription Map (Black = Spray Hotspots)")

plt.tight_layout()
plt.show()