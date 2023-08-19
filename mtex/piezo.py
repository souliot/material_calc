import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 压电矩阵
d = np.loadtxt("./mtex/piezo.csv", dtype=np.float64)

print(d)

# 构造示性曲面坐标点
E_values = np.linspace(-10, 10, 100)  # 电场范围
sigma_values = np.linspace(-10, 10, 100)  # 应力范围
E, sigma = np.meshgrid(E_values, sigma_values)

P = np.zeros_like(E)  # 初始化电荷极化
print(E.shape)
print(P.shape)

for i in range(3):
  for j in range(6):
    P += d[i, j] * E**i * sigma**j

print(P.shape)

# 绘制示性曲面
fig = plt.figure()
# ax = Axes3D(fig)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(E, sigma, P, cmap='viridis')
ax.set_xlabel('Electric Field (E)')
ax.set_ylabel('Stress (sigma)')
ax.set_zlabel('Polarization (P)')

plt.show()
