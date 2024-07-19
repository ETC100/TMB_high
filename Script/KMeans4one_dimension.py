# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:14:16 2024

@author: Administrator
"""
import numpy as np
import pandas as pd


df = pd.read_table(r'C:\Users\Administrator\Desktop\tmb715.txt', sep='\t')
data = df['TMB_score'].values
Y = df.groupby('cancer_type').size() / df.groupby('cancer_type').size().sum()
df = pd.merge(df, Y.rename('weight'), on="cancer_type")
weights = np.array(df['weight'].astype(float))

def kmeans_1d(data, k, weights, max_iter=200):
    # 随机初始化聚类中心
    centroids = np.random.choice(data, k, replace=False)
    
    for _ in range(max_iter):
        # 分配数据点到最近的聚类中心
        labels = np.argmin(np.abs(data[:, np.newaxis] - centroids), axis=1)
        
        # 更新聚类中心
        # new_centroids = np.array([np.mean(data[labels == i]) for i in range(k)])
        new_centroids = np.array([np.average(data[labels == i], weights=weights[labels == i]) for i in range(k)])
        
        # 判断聚类中心是否收敛
        if np.array_equal(new_centroids, centroids):
            break
        
        centroids = new_centroids
    
    return centroids, labels

# 生成一维数据
data = np.random.rand(100)
k = 2

# 调用自定义的 K-means 函数
centroids, labels = kmeans_1d(data, k, weights)

print("聚类中心:", centroids)
print("每个数据点的类别:", labels)
