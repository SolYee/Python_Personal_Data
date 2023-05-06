"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/6 9:18
# @Author:Szeto YiZe
# @File:HandwrittenDigitalPicture.py
# @Update:
"""
# 导入相关库
import torch
import torch.nn as n
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np


# 定义生成器
class Generator(n.Module):

    def __init__(self, latent_dim, img_shape):
        super(Generator, self).__init__()

        self.img_shape = img_shape
        self.fc = n.Linear(latent_dim, 128)
        self.conv1 = n.Conv2d(128, 256, 4, 2, 1)
        self.conv2 = n.Conv2d(256, 512, 4, 2, 1)
        self.conv3 = n.Conv2d(512, 1024, 2, 1)
        self.conv4 = n.Conv2d(1024, self.img_shape[0], 4, 2, 1)

    def forward(self, x):
        x = F.leaky_relu(self.fc(x), 0.2)

        x = x.view(-1, 128, 4)
        x = F.leaky_relu(self.conv1(x), 0.2)
        x = F.leaky_relu(self.conv2(x), 0.2)
        x = F.leaky_relu(self.conv3(x), 0.2)
        x = torch.tanh(self.conv4(x))

        return x


# 定义判别器
class Discriminator(n.Module):

    def __init__(self, img_shape):
        super(Discriminator, self).__init__()
        self.img_shape = img_shape
        self.conv1 = n.Conv2d(self.img_shape[0], 512, 4, 2, 1)
        self.conv2 = n.Conv2d(512, 256, 4, 2, 1)
        self.conv3 = n.Conv2d(256, 128, 4, 2, 1)
        self.fc = n.Linear(128 * 4, 1)

    def forward(self, x):
        x = F.leaky_relu(self.conv1(x), 0.2)
        x = F.leaky_relu(self.conv2(x), 0.2)
        x = F.leaky_relu(self.conv3(x), 0.2)
        x = x.view(-1, 128 * 4)
        x = self.fc(x)
        return x


# 定义损失函数
def los_func(real_score, fake_score):
    real_los = torch.mean((real_score - 1) * 2)
    fake_los = torch.mean(fake_score * 2)
    return real_los + fake_los


# 定义训练函数
def train(dataloader, discriminator, generator, device, optimizer_d, optimizer_g, los_func):
    discriminator.train()
    generator.train()
    for real_img, _ in dataloader:
        batch_size = real_img.size(0)
    real_img = real_img.to(device)
    # 训练判别器
    optimizer_d.zero_grad()
    # 生成噪声
    z = torch.randn(batch_size, latent_dim).to(device)
    # 生成假图片
    fake_img = generator(z)
    # 计算真实图片的分数
    real_score = discriminator(real_img)
    # 计算假图片的分数
    fake_score = discriminator(fake_img)
    # 计算损失
    d_los = los_func(real_score, fake_score)
    # 反向传播
    d_los.backward()
    optimizer_d.step()
    # 训练生成器
    optimizer_g.zero_grad()
    # 生成噪声
    z = torch.randn(batch_size, latent_dim).to(device)
    # 生成假图片
    fake_img = generator(z)
    # 计算假图片的分数
    fake_score = discriminator(fake_img)
    # 计算损失
    g_los = los_func(real_score, fake_score)
    # 反向传播
    g_los.backward()
    optimizer_g.step()


# 定义可视化函数
def visualize(generator, device, n_row=5, figsize=(5, 5)):
    generator.eval()
    # 生成噪声
    z = torch.randn(n_row * 2, latent_dim).to(device)
    # 生成假图片
    fake_img = generator(z)
    # 可视化
    fig, axes = plt.subplots(n_row, figsize=figsize)
    for ax, img in zip(axes.flaten(), fake_img):
        ax.axis('of')
    ax.set_adjustable('box-forced')
    ax.imshow(img.cpu().data.view(img_shape).numpy(), cmap='gray', aspect='equal')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
    # 定义参数
    img_shape = (1, 28)
    latent_dim = 10
    # 加载数据
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5,), std=(0.5,))
    ])
    dataloader = DataLoader(
        datasets.MNIST('data', train=True, download=True, transform=transform),
        batch_size=64,
        shufle=True
    )
    # 定义模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    generator = Generator(latent_dim, img_shape).to(device)
    discriminator = Discriminator(img_shape).to(device)
    # 定义优化器
    optimizer_d = optim.Adam(discriminator.parameters(), lr=0.02, betas=(0.5, 0.9))
    optimizer_g = optim.Adam(generator.parameters(), lr=0.02, betas=(0.5, 0.9))
    # 训练模型
    epochs = 20
    for epoch in range(epochs):
        train(dataloader, discriminator, generator, device, optimizer_d, optimizer_g, los_func)
    if epoch % 10 == 0:
        print(
            f'epoch: {epoch}, d_los: {train.d_los.item()}, g_los: {train.g_los.item()}'
        )
    # 可视化
    visualize(generator, device)
