class Period:
    half_period = 180
    period = 360


def periodic_distance(angle, median):
    result = min(abs(median - angle), Period.period - (abs(median - angle)))
    return result


def subtract_two_angles(angle1, angle2):
    return float(abs(angle1 - angle2))


def clone_angle(median, angle):
    if median < angle:
        return angle - Period.period
    else:
        return angle + Period.period


def angle_in_the_range(angle, median):
    lower_bound = median - Period.half_period
    upper_bound = median + Period.half_period
    if (lower_bound <= angle <= upper_bound):
        return angle
    elif (lower_bound > angle):
        return angle + Period.period
    else:
        return angle - Period.period

