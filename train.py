from torch.utils.data import DataLoader
from model import NBAClassifier, weights_init
from dataset import NBADataset, MusicDataset
import torch
from torch import nn
import matplotlib.pyplot as plt


def train(train_dataset, test_dataset, n_epochs, display_epoch, pretrained=False, batch_size=8, loss_function=nn.CrossEntropyLoss()):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    NBA_Classifier = NBAClassifier().to(device)

    if pretrained:
        NBA_Classifier.load_state_dict(torch.load("预训练参数pth文件路径"))
    else:
        NBA_Classifier = NBA_Classifier.apply(weights_init)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    optimizer = torch.optim.Adam(NBA_Classifier.parameters(), lr=0.001)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 200, gamma=0.9)

    loss_all = []
    epochs = []
    step = 0
    best_test_acc = 0

    for epoch in range(n_epochs):
        loss_sum = 0
        train_right = 0
        train_false = 0
        for x, y in train_dataloader:
            x = x.to(device)
            y = y.to(device)

            NBA_Classifier.train()
            optimizer.zero_grad()

            y_ = NBA_Classifier(x)


            loss = loss_function(y_, y)

            loss.backward()
            optimizer.step()


            output = torch.argmax(y_, dim=1)
            train_count_right = output == y
            train_count_false = output != y
            train_right += sum(train_count_right)
            train_false += sum(train_count_false)
            loss_sum += loss
            step += 1
        loss_all.append(float(loss_sum))
        epochs.append(epoch)

        lr_scheduler.step()

        if epoch % display_epoch == 0:
            with torch.no_grad():
                NBA_Classifier.eval()
                test_right = 0
                test_false = 0
                for x1, y1 in test_dataloader:
                    x1 = x1.to(device)
                    y1 = y1.to(device)

                    y1_ = NBA_Classifier(x1)

                    output1 = torch.argmax(y1_, dim=1)
                    test_count_right = output1 == y1
                    test_count_false = output1 != y1
                    test_right += sum(test_count_right)
                    test_false += sum(test_count_false)

                test_acc = test_right / (test_right + test_false)

                if test_acc > best_test_acc:
                    best_test_acc = test_acc
                    torch.save(NBA_Classifier.state_dict(), "./output/%s_%d.pth" % ("NBA_Classifier_best_test", step))

            print(f"Epoch {epoch}: Step {step}: NBA_Classifier loss: {loss_sum}, 训练集正确数量: {train_right}, "
                  f"训练集错误数量: {train_false}, NBA_Classifier训练集准确率: {train_right / (train_right + train_false)} "
                  f"Learning rate: {optimizer.param_groups[0]['lr']}")
            print(f"测试集正确数量: {test_right}, 测试集错误数量: {test_false}, "
                  f"NBA_Classifier测试集准确率: {test_acc} ")

    torch.save(NBA_Classifier.state_dict(), "./output/%s_%d.pth" % ("NBA_Classifier", step))

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.set_xlabel('epoch')
    ax1.set_ylabel('loss')
    ax1.set_title("Loss picture")

    ax1.plot(epochs, loss_all)

    plt.savefig('Loss_chart1.jpg')
    plt.show()


train_dataset = NBADataset('./data/data_rest_twoclass.npy')
test_dataset = NBADataset('./data/data_2021_twoclass.npy')
train(train_dataset, test_dataset, n_epochs=1000, display_epoch=10, pretrained=False, batch_size=8, loss_function=nn.CrossEntropyLoss())
