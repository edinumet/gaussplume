def overlay_on_map(x,y,C1):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.image as mpimg
    
    # Overlay concentrations on map
    plt.ion()
    plt.figure()
    img = mpimg.imread('Mossmorran_3_km-radius.png')
    imgplot = plt.imshow(img, extent=(-3000, 3000, -3000, 3000))
    plt.xlabel('x (metres)')
    plt.ylabel('y (metres)')
    cs = plt.contour(x, y, np.mean(C1, axis=2) * 1e6, cmap='Blues')
    plt.clabel(cs, cs.levels, inline=True, fmt='%.1f', fontsize=5)
    plt.show()
    plt.savefig("Mossmorran_Concentrations.png")
    return
    
if __name__  ==  "__main__":
    overlay_on_map()
