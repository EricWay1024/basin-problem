import basin
import numpy as np
import nevis
import random

data = nevis.gb()
vmin = np.min(data)
vmax = np.max(data)

def get_part(data, size):
    m, n = data.shape
    # find the largest entry index in the matrix
    max_idx = np.argmax(data)
    # # save a 40x40 submatrix centered at the largest entry as text file
    size //= 2
    part = data[max_idx // n - size: max_idx // n + size, max_idx % n - size: max_idx % n + size]
    return part

part = get_part(data, 160)
np.savetxt('part.txt', part, fmt='%.1f')


def find_labels(h):
    maxima, sn = basin.find_maxima(h)
    np.savetxt('maxima.txt', maxima, fmt='%d')
    np.savetxt('sn.txt', sn, fmt='%d')
    label = basin.find_basins(h, sn, maxima)
    return label, maxima

def plot_label(h, label, maxima, show_max_num=None):
    import matplotlib.pyplot as plt
    import matplotlib.colors

    f = lambda x: (x - vmin) / (vmax - vmin)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'soundofmusic', [
        (0, '#4872d3'),             # Deep sea blue
        (f(-0.1), '#68b2e3'),       # Shallow sea blue
        (f(0.0), '#0f561e'),        # Dark green
        (f(10), '#1a8b33'),         # Nicer green
        (f(100), '#11aa15'),        # Glorious green
        (f(300), '#e8e374'),        # Yellow at ~1000ft
        (f(610), '#8a4121'),        # Brownish at ~2000ft
        (f(915), '#999999'),        # Grey at ~3000ft
        (1, 'white'),
    ], N=1024)

    plt.imshow(
        h, 
        origin='lower',
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        interpolation='none',
    )

    if show_max_num is not None:
        label[label >= show_max_num] = show_max_num
    
    num_colors = len(np.unique(label))
    cmap = plt.get_cmap('gist_ncar', num_colors)
    indices = list(range(num_colors))
    random.seed(12138)
    random.shuffle(indices)
    cmap_object = matplotlib.colors.ListedColormap([cmap(i) for i in indices])


    plt.imshow(
        label,
        origin='lower',
        # cmap='tab20',
        cmap=cmap_object,
        interpolation='none',
        alpha=1,
    )

    # if show_max_num is not None:
    #     x, y = maxima[:show_max_num].T
    # else:
    x, y = maxima.T
    
    plt.scatter(y[1:], x[1:], c='white', s=50, marker='x')
    plt.scatter(y[:1], x[:1], c='red', s=50, marker='x')
    plt.show()

label, maxima = find_labels(part)
np.savetxt('label.txt', label, fmt='%d')
plot_label(part, label, maxima, show_max_num=None)
