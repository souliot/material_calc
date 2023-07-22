import numpy as np
import matplotlib.pyplot as plt
import os

from material_calc.util.logger import logs


def polarDatas(ax, plane, datas, title, col=1):
  th = datas[:, 0]
  theta = th * np.pi / 180
  r = datas[:, col]
  ax.set_title(title, y=-0.25)
  ax.plot(theta, r, "-", linewidth=1.5, label=plane)
  ax.fill(theta, r, alpha=0.2)
  return


def polar(dir, ax, type, title):
  col = 1
  if type == "bulk":
    col = 2

  # 001
  datas001 = np.loadtxt("{}/DatFile_001/2dcut_{}.dat".format(dir, type), dtype=np.float64)
  polarDatas(ax, '001', datas001, title, col)

  # 010
  datas010 = np.loadtxt("{}/DatFile_010/2dcut_{}.dat".format(dir, type), dtype=np.float64)
  polarDatas(ax, '010', datas010, title, col)

  # 100
  datas100 = np.loadtxt("{}/DatFile_100/2dcut_{}.dat".format(dir, type), dtype=np.float64)
  polarDatas(ax, '100', datas100, title, col)
  return


def ploar_item(dir, name):
  out_path = "{}/{}".format(dir, "img_n1")

  output_img = "{}/{}.png".format(out_path, name)
  if os.path.exists(output_img):
    return output_img

  if not os.path.exists(out_path):
    os.makedirs(out_path)

  plt.style.use([r'/app/libs/stylelib/xy.mplstyle', r'/app/libs/stylelib/no-latex.mplstyle',])
  fig = plt.figure(dpi=600, figsize=(9, 7))
  e = fig.add_subplot(2, 3, 1, projection="polar")
  polar(dir,  e, "young", title="(E)")

  b = fig.add_subplot(2, 3, 2, projection="polar")
  polar(dir,  b, "bulk", title="(B)")

  g = fig.add_subplot(2, 3, 3, projection="polar")
  polar(dir,  g, "shear", title="(G)")

  po = fig.add_subplot(2, 3, 4, projection="polar")
  polar(dir,  po, "poisson", title="(σ)")

  pu = fig.add_subplot(2, 3, 5, projection="polar")
  polar(dir,  pu, "pugh", title="(B/G)")

  plt.tight_layout()
  plt.legend(bbox_to_anchor=(2, 0.65))
  output_img = "{}/{}/{}.png".format(dir, "img_n1", name)
  plt.savefig(output_img)
  logs.info("plot success file to: {}".format(output_img))
  return output_img
