import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

t = np.linspace(0, 4 * np.pi, 100000)
x1 = np.cos(t)
x2 = np.cos(6.5 * t)

y1 = np.sin(t)
y2 = np.sin(6.5 * t)

x = 13 * (x1 - x2 / 6.5)
y = 13 * (y1 - y2 / 6.5)

fig = plt.figure(figsize=(5, 5))
plt.plot(x, y)

plt.savefig("img_1.png")

img1 = Image.open("img_1.png")
img1 = img1.convert("L")
img1 = img1.save("img_result.bmp")

plt.show()
