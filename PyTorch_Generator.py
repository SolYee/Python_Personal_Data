"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/8 10:43
# @Author:Szeto YiZe
# @File:PyTorch_Generator.py
# @Update:使用 PyTorch 实现 GAN 生成手写数字图片的代码
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


# 定义生成器
class Generator(nn.Module):

    def __init__(self, latent_dim=100, img_shape=(1, 28, 28)):
        super(Generator, self).__init__()
        self.latent_dim = latent_dim
        self.img_shape = img_shape
        self.fc1 = nn.Linear(self.latent_dim, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 512)
        self.fc4 = nn.Linear(512, 1024)
        self.fc5 = nn.Linear(1024, int(torch.prod(torch.tensor(self.img_shape))))

    def forward(self, x):
        x = x.view(-1, self.latent_dim)
        x = nn.functional.leaky_relu(self.fc1(x), 0.2)
        x = nn.functional.leaky_relu(self.fc2(x), 0.2)
        x = nn.functional.leaky_relu(self.fc3(x), 0.2)
        x = nn.functional.leaky_relu(self.fc4(x), 0.2)
        x = torch.tanh(self.fc5(x))
        x = x.view(-1, *self.img_shape)
        return x


# 定义判别器
class Discriminator(nn.Module):

    def __init__(self, img_shape=(1, 28, 28)):
        super(Discriminator, self).__init__()
        self.img_shape = img_shape
        self.fc1 = nn.Linear(int(torch.prod(torch.tensor(self.img_shape))), 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 1)

    def forward(self, x):
        x = x.view(-1, int(torch.prod(torch.tensor(self.img_shape))))
        x = nn.functional.leaky_relu(self.fc1(x), 0.2)
        x = nn.functional.leaky_relu(self.fc2(x), 0.2)
        x = torch.sigmoid(self.fc3(x))
        return x


# 定义超参数
batch_size = 128
latent_dim = 100
img_shape = (1, 28, 28)
lr = 0.0002
betas = (0.5, 0.999)
epochs = 100

# 加载MNIST数据集
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# 初始化生成器和判别器
G = Generator(latent_dim, img_shape)
D = Discriminator(img_shape)

# 定义优化器和损失函数
g_optimizer = optim.Adam(G.parameters(), lr=lr, betas=betas)
d_optimizer = optim.Adam(D.parameters(), lr=lr, betas=betas)
criterion = nn.BCELoss()

# 训练模型
G.train()
D.train()
for epoch in range(epochs):
    for i, (real_imgs, _) in enumerate(train_loader):
        # 训练判别器
        d_optimizer.zero_grad()
        real_imgs = real_imgs.cuda()
        real_labels = torch.ones(real_imgs.size(0), 1).cuda()
        fake_labels = torch.zeros(real_imgs.size(0), 1).cuda()
        # 生成噪声
        z = torch.randn(real_imgs.size(0), latent_dim).cuda()
        fake_imgs = G(z)
        # 判别器判别真实图片
        real_scores = D(real_imgs)
        d_loss_real = criterion(real_scores, real_labels)
        # 判别器判别假图片
        fake_scores = D(fake_imgs.detach())
        d_loss_fake = criterion(fake_scores, fake_labels)
        # 计算判别器损失
        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        d_optimizer.step()
        # 训练生成器
        g_optimizer.zero_grad()
        # 重新生成假图片
        fake_imgs = G(z)
        # 判别器判别生成的假图片
        fake_scores = D(fake_imgs)
        g_loss = criterion(fake_scores, real_labels)
        g_loss.backward()
        g_optimizer.step()
