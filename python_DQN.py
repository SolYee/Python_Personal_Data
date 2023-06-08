"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/8 18:01
# @Author:YiShouquan
# @File:python_DQN.py
# @Update:
"""

import random
import numpy as np
import tensorflow as tf

# 定义排序问题的状态和动作
num_items = 10
state_size = num_items * 2  # 待排序序列中元素的值和位置信息
action_size = num_items * (num_items - 1) // 2  # 交换两个元素的位置


# 定义深度Q网络模型
class DQNSortModel(tf.keras.Model):
    def __init__(self, state_size, action_size):
        super(DQNSortModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(32, activation='relu', input_dim=state_size)
        self.dense2 = tf.keras.layers.Dense(32, activation='relu')
        self.dense3 = tf.keras.layers.Dense(action_size, activation='linear')

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        q_values = self.dense3(x)
        return q_values


# 定义强化学习算法
class DQNSortAlgorithm:
    def __init__(self, state_size, action_size, discount_factor=0.95, epsilon=1.0, epsilon_min=0.01,
                 epsilon_decay=0.995,
                 learning_rate=0.001, batch_size=32, memory_size=1000):
        self.state_size = state_size
        self.action_size = action_size
        self.discount_factor = discount_factor  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.epsilon_min = epsilon_min  # 最小探索率
        self.epsilon_decay = epsilon_decay  # 探索率衰减因子
        self.learning_rate = learning_rate  # 学习率
        self.batch_size = batch_size  # 批量大小
        self.memory = []  # 记忆回放
        self.memory_size = memory_size  # 记忆回放大小
        self.model = DQNSortModel(self.state_size, self.action_size)  # DQN模型
        self.optimizer = tf.keras.optimizers.Adam(lr=self.learning_rate)  # Adam优化器
        self.loss_fn = tf.keras.losses.MeanSquaredError()  # 均方误差损失函数

    # 选择动作
    def select_action(self, state):
        if np.random.rand() <= self.epsilon:
            # 探索
            return random.randrange(self.action_size)
        else:
            # 开发
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])

    # 记忆回放
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    # 训练DQN模型
    def train_model(self):
        if len(self.memory) < self.batch_size:
            return
        # 从记忆回放中随机选择一批数据
        minibatch = random.sample(self.memory, self.batch_size)
        states = np.zeros((self.batch_size, self.state_size))
        next_states = np.zeros((self.batch_size, self.state_size))
        actions, rewards, dones = [], [], []
        for i in range(self.batch_size):
            states[i] = minibatch[i][0]
            actions.append(minibatch[i][1])
            rewards.append(minibatch[i][2])
            next_states[i] = minibatch[i][3]
            dones.append(minibatch[i][4])

        # 计算Q值
        q_values = self.model.predict(states)
        next_q_values = self.model.predict(next_states)
        for i in range(self.batch_size):
            q_values[i][actions[i]] = rewards[i] + self.discount_factor * np.max(next_q_values[i]) * (1 - dones[i])

        # 更新DQN模型
        self.model.train_on_batch(states, q_values)

    # 降低探索率
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # 定义测试函数
    def test_DQNSortAlgorithm(sort_algorithm):
        # 创建DQNSortAlgorithm对象
        dqn = DQNSortAlgorithm(state_size, action_size)
        # 创建随机状态
        state = np.random.rand(1, state_size)
        # 选择动作
        action = dqn.select_action(state)
        # 记忆回放
        reward = 1
        next_state = np.random.rand(1, state_size)
        done = False
        dqn.remember(state, action, reward, next_state, done)
        # 训练DQN模型
        dqn.train_model()
        # 降低探索率
        dqn.decay_epsilon()
