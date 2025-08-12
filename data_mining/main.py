# %%
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler

import pandas as pd
import pickle
from tqdm import tqdm

from ucimlrepo import fetch_ucirepo 

# # 下载数据集并保存至本地
# rt_iot2022 = fetch_ucirepo(id=942) 
# pickle.dump(rt_iot2022, open("rt_iot2022.pkl", "wb"))

rt_iot2022 = pickle.load(open("rt_iot2022.pkl", "rb"))

# data (as pandas dataframes)
X = rt_iot2022.data.features
y = rt_iot2022.data.targets

# 删除 service 属性
X = X.drop(columns=["service"])
print("初始 X 形状：", X.shape)

# 将 proto 属性独热编码
df_encoded = pd.get_dummies(X, columns=["proto"])
print("对 proto 独热编码后的形状：", df_encoded.shape)
print("对 proto 独热编码后的 head():", df_encoded.head())
X = df_encoded

kf = KFold(n_splits=10, shuffle=True)

# %% KNN
all_accuracies = []
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    all_accuracies.append(accuracy)

print("KNN 准确率：", sum(all_accuracies) / len(all_accuracies))

# %% CART 决策树
all_accuracies = []
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    y_pred = dt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    all_accuracies.append(accuracy)

print("CART 决策树准确率：", sum(all_accuracies) / len(all_accuracies))

# %% 随机森林
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    all_accuracies.append(accuracy)

print("随机森林准确率：", sum(all_accuracies) / len(all_accuracies))


# %% DNN
class DNN(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(DNN, self).__init__()
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_sizes) - 1):
            self.hidden_layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
        self.output_layer = nn.Linear(hidden_sizes[-1], output_size)

    def forward(self, x):
        for layer in self.hidden_layers:
            x = torch.relu(layer(x))
        x = self.output_layer(x)
        return x

hidden_sizes = [X.shape[1], 64]


all_accuracies = []
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    model = DNN(X.shape[1], hidden_sizes, y["Attack_type"].nunique())
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # 标准化数据数据
    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)
    # 使用类别索引进行特征类别转化
    y_train_cat = y_train["Attack_type"].astype("category").cat.codes
    y_test_cat = y_test["Attack_type"].astype("category").cat.codes
    # # print(y_train_cat.head())
    # print(y_test_cat.head())
    # # 输出类别总数
    # print(y_train_cat.nunique())

    # 转为 PyTorch 的 Tensor 格式
    X_train_tensor = torch.tensor(X_train_std, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test_std, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train_cat.values, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test_cat.values, dtype=torch.long)

    # 创建数据加载器
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # 训练模型
    num_epochs = 10
    for epoch in tqdm(range(num_epochs)):
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # 在测试集上评估模型
    model.eval()
    with torch.no_grad():
        outputs = model(X_test_tensor)
        _, predicted = torch.max(outputs, 1)
        accuracy = (predicted == y_test_tensor).sum().item() / len(y_test)
        all_accuracies.append(accuracy)
    print(f"准确率：{accuracy}")

print("DNN 准确率（总体）：", sum(all_accuracies) / len(all_accuracies))
