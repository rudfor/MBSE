#!/usr/bin/env python
import geopandas as gpd
import matplotlib.pyplot as plt

# Import all roads NL
map_df = gpd.read_file('roads.shp')
# Show data format
map_df.head()

# Set image properties
fig, ax = plt.subplots(1, figsize=(10,14))
map_df.plot(cmap='Wistia', ax=ax)
ax.axis('off')

# Set coordinates to match Utrecht, change for your own city
ax.set_xlim(5.1050, 5.1400)
ax.set_ylim(52.0620, 52.1115)
ax.set_aspect('equal')

# Plot the street map of Utrecht
plt.show()