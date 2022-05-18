import matplotlib.pyplot as plt
import numpy as np

arr = [(286, 339),
       (285, 334),
       (286, 331),
       (315, 328),
       (315, 326),
       (285, 326),
       (272, 321),
       (272, 315),
       (268, 308),
       (257, 298),
       (272, 287),
       (268, 282),
       (273, 275),
       (269, 269),
       (268, 262),
       (278, 252),
       (282, 252),
       (295, 249)]

x = np.array([])
y = np.array([])

for i in arr:
    print(i)
    x = np.append(x, i[0])
    y = np.append(y, i[1])

# x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
# y = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])

plt.scatter(x, y)
plt.show()
