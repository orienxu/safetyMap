import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset

import warnings

warnings.filterwarnings("ignore")
plt.ion()

class SeattleCrime(Dataset):
    def __init__(self, transform=None):
        data = pd.read_csv('crime_data.csv')
        data['Offense Start DateTime'] = pd.to_datetime(data['Offense Start DateTime'])
        unfiltered = data[['Offense Start DateTime', 'Latitude', 'Longitude']].dropna()
        mask = (unfiltered['Latitude'] != 0.) & (unfiltered['Longitude'] != 0.)
        data = unfiltered[mask]

        self.transform = transform
        self.inputs = np.ndarray((data.shape[0], 4))
        # self.inputs[:, 0] = data['Offense Start DateTime'].dt.year.to_numpy()
        self.inputs[:, 0] = data['Offense Start DateTime'].dt.month.to_numpy()
        self.inputs[:, 1] = data['Offense Start DateTime'].dt.day.to_numpy()
        self.inputs[:, 2] = data['Offense Start DateTime'].dt.hour.to_numpy()
        self.inputs[:, 3] = data['Offense Start DateTime'].dt.minute.to_numpy()
        self.labels = data[['Latitude', 'Longitude']].to_numpy()
        self.labels[:, 0] -= 47.6
        self.labels[:, 1] += 122.3
        print('loaded')


    def __len__(self):
        return self.inputs.shape[0]


    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        return torch.from_numpy(self.inputs[idx]), torch.from_numpy(self.labels[idx])
