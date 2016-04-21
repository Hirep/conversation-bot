import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
digits = load_digits()


n_row, n_col = 2,5

def print_digits(images, y, max_n=10):
    fig = plt.figure(figsize=(2.*n_col, 2.26*n_row))
    i = 0
    while i < max_n and i < images.shape[0]:
        p = fig.add_subplot(n_row, n_col, i+1, xticks=[],
                            yticks=[])
        p.imshow(images[i],
                 # cmap=plt.cm.bone,
                 interpolation='nearest')
        p.text(0,-1,str(y[i]))
        i = i+1

print_digits(digits.images, digits.target, max_n=10)
plt.show()