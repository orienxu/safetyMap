import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(4, 8)
        self.fc2 = nn.Linear(8, 8)
        # self.fc3 = nn.Linear(16, 16)
        # self.fc4 = nn.Linear(16, 16)
        # self.fc5 = nn.Linear(8, 8)
        self.fc6 = nn.Linear(8, 2)
        # self.d1 = nn.Dropout(p=0.2)
        # self.d2 = nn.Dropout(p=0.1 )

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = F.relu(self.fc4(x))
        # x = self.d1(x)
        # x = F.relu(self.fc5(x))
        # x = self.d2(x)
        x = self.fc6(x)
        return x