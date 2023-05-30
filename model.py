from torch import nn
import torch
# import torchinfo


class NBAClassifier(nn.Module):
    def __init__(self):
        super(NBAClassifier, self).__init__()

        #v1
        self.layer1 = nn.Linear(51, 150)
        self.layer2 = nn.Linear(150, 75)
        self.layer3 = nn.Linear(75, 25)
        self.layer4 = nn.Linear(25, 2)

        self.dropout1 = nn.Dropout(p=0.15)
        self.dropout2 = nn.Dropout(p=0.15)
        self.dropout3 = nn.Dropout(p=0.15)

        self.BN0 = nn.BatchNorm1d(51, momentum=0.5)
        self.BN1 = nn.BatchNorm1d(150, momentum=0.5)
        self.BN2 = nn.BatchNorm1d(75, momentum=0.5)
        self.BN3 = nn.LayerNorm(25)

        self.activation1 = nn.Tanh()
        self.activation2 = nn.LeakyReLU(0.02)
        self.activation3 = nn.ReLU()

    def forward(self, x):
        x = self.BN0(x)
        x = self.layer1(x)
        x = self.activation1(x)
        x = self.dropout1(x)

        x = self.BN1(x)
        x = self.layer2(x)
        x = self.activation1(x)
        x = self.dropout2(x)

        x = self.BN2(x)
        x = self.layer3(x)
        x = self.activation1(x)
        x = self.dropout3(x)

        x = self.BN3(x)
        x = self.layer4(x)
        x = self.activation2(x)

        return x


# model = NBAClassifier()
# torchinfo.summary(model, input_size=(1, 45))

def weights_init(m):
    # instance(object，type)函数判断一个object是否是type类型
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_in')
