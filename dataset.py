import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np


class NBADataset(Dataset):

    def __init__(self, NBA_data_dir):
        super(NBADataset, self).__init__()
        # data = pd.read_csv(NBA_data_dir)
        # data['label'] = pd.factorize(data.label)[0]
        data = np.load(NBA_data_dir)
        print(data.shape)
        # x_data = data.iloc[:, 3:-1].values
        # y_data = data.iloc[:, -1].values
        x_data = data[:, 1:]
        y_data = data[:, 0]

        self.x_data = torch.from_numpy(x_data).type(torch.float32)
        self.y_data = torch.from_numpy(y_data).type(torch.int64)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, index):
        x_data = self.x_data[index]
        y_data = self.y_data[index] - torch.ones_like(self.y_data[index])
        return x_data, y_data.long()


class MusicDataset(Dataset):

    def __init__(self, music_data_dir):
        super(MusicDataset, self).__init__()
        data = pd.read_csv(music_data_dir)
        data['genres'] = pd.factorize(data.genres)[0]
        # data = np.load(NBA_data_dir)

        x_data = data.iloc[:, 8:19].values
        x_data = x_data.astype(float)
        print(x_data.shape)
        y_data = data.iloc[:, -1].values
        # x_data = data[:, 0:-1]
        # y_data = data[:, -1]

        self.x_data = torch.from_numpy(x_data).type(torch.float32)
        self.y_data = torch.from_numpy(y_data).type(torch.int64)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, index):
        x_data = self.x_data[index]
        y_data = self.y_data[index] # - torch.ones_like(self.y_data[index])
        return x_data, y_data.long()