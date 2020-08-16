import pandas as pd
import numpy as np
import gmaps
import gmaps.datasets

gmaps.configure('AIzaSyA_BHVdY4te69lUs4b-KZOo0aSnqwXBg00')

crime= pd.read_csv("crime_data.csv")
crime.head()
# print(crime['Longitude'][14])

# Lat = np.arange(47.545, 47.714, 0.00169)
# Lon = np.arange(-122.452, -122.231, 0.00221)

# Crime_counts = np.zeros((100,100))
#
# for a in range(len(crime)):
#
#   for b1 in range(100):
#
#       if Lat[b1] – 0.00105 <= crime_2018[‘lat’].values[a] < Lat[b1] + 0.00105:
#
#   for b2 in range(100):
#
#     if Lon[b2] – 0.00119 <= crime_2018[‘long’].values[a] < Lon[b2] + 0.00119:
#
#         Crime_counts[b1,b2] += 1
#
# latitude_values = np.repeat(Lat,100)
# longitude_values = [Lon,]*100
# Crime_counts.resize((10000,))
#
# heatmap_data = {'Counts': Crime_counts, 'latitude': latitude_values, 'longitude' : np.concatenate(longitude_values)}
# df = pd.DataFrame(data=heatmap_data)
#
# locations = df[['latitude', 'longitude']]
# weights = df['Counts']
# fig = gmaps.figure()
# heatmap_layer = gmaps.heatmap_layer(locations, weights=weights)
# fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))

# locations=crime[['Latitude', 'Longitude']]
# data = [tuple(x) for x in locations.values]
# fig = gmaps.figure(map_type='HYBRID')
# heatmap_layer = gmaps.Heatmap(locations=data)
# fig.add_layer(heatmap_layer)
# fig

crime['Offense Start DateTime'] = pd.to_datetime(crime['Offense Start DateTime'])
unfiltered =crime[['Offense Start DateTime', 'Latitude', 'Longitude']].dropna()
# unfiltered = crime.dropna()

print('Unfiltered length: ', len(unfiltered))

mask = (unfiltered['Latitude'] != 0.) & (unfiltered['Longitude'] != 0.)
filtered = unfiltered[mask]

print('Filtered length: ', len(filtered))