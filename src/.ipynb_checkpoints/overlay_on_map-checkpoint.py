def overlay_on_map(x,y,C1):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.image as mpimg
    
    # Overlay concentrations on map
    plt.ion()
    plt.figure()
    img = mpimg.imread('Alicante.png')
    imgplot = plt.imshow(img, extent=(-2500, 2500, -2500, 2500))
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    cs = plt.contour(x, y, np.mean(C1, axis=2)*1e6, cmap='hot')
    plt.clabel(cs, cs.levels, inline=True, fmt='%.1f', fontsize=5)
    plt.show()
    plt.savefig("Alicante_Concentrations.png")
    return
    
if __name__  ==  "__main__":
    overlay_on_map()
