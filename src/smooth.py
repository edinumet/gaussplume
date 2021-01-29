def smooth(y, box_pts):
    """
    :param y:
    :param box_pts:
    :return:
    docstring """
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth