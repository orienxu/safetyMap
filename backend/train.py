from torch.utils.data import Dataset
import torch.nn as nn
import torch.optim as optim
from load import *
from model import Net
import warnings


warnings.filterwarnings("ignore")
plt.ion()

def train(model, criterion, optimizer, train_loader, device, num_epochs, log_interval):
    model.train()
    for epoch in range(num_epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.float().cuda().to(device), target.float().cuda().to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))
    return model

def main():

    dataset = SeattleCrime()

    dataloader = torch.utils.data.DataLoader(dataset, batch_size=64,
                                                        shuffle=True)
    device = torch.device("cuda")

    model = Net()

    model = model.to(device)


    optimizer_conv = optim.Adam(model.parameters(), lr=0.00003)

    criterion = nn.MSELoss()
    epochs = 1
    model = train(model, criterion, optimizer_conv, dataloader, device, num_epochs=epochs, log_interval=1000)

    torch.save(model.state_dict(), './trained_model.pth')

if __name__ == '__main__':
    main()
