import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义空间坐标范围
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
z = np.linspace(-1, 1, 100)

# 生成网格
X, Y, Z = np.meshgrid(x, y, z)

# 定义纵向压电模量向量K"""  """
K = np.array([[[1e9, 0, 0],
              [0, 1e9, 0],
              [0, 0, 1e9]],
             [[2e9, 0, 0],
              [0, 2e9, 0],
              [0, 0, 2e9]],
             [[3e9, 0, 0],
              [0, 3e9, 0],
              [0, 0, 3e9]]])

# 绘制纵向压电模量的三维示性曲面
fig = plt.figure()
ax = Axes3D(fig)
ax.quiver(X[..., np.newaxis], Y[..., np.newaxis], Z[..., np.newaxis], K[0], K[1], K[2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
