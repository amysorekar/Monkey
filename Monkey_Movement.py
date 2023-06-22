import math


def midpoints(list):
    """
    Takes a list of raw data (in the 3d form of frame, 3 points per frame (L ear
    R ear, nose), 2 coordinates per point), isolates the 2 ear points, and gets the
    midpoint between the 2.

    Parameters
    ----------
    list : a list of raw data

    Returns
    -------
    midpoints : a list of midpoints between the two ears

    """

    midpoints = []

    for line in list:
        avg_x = (line[0][0] + line[1][0]) / 2
        avg_y = (line[0][1] + line[1][1]) / 2
        midpoint = [avg_x, avg_y]
        midpoints.append(midpoint)

    return midpoints


def distance(midpoints, start, end):
    """
    calculates the distance between the midpoint at the start of a speaker
    call and the midpoint at the end of a speaker call

    Parameters
    ----------
    midpoints : a list of midpoints

    start : a list of start times of speaker calls

    end : a list of end times of speaker calls

    Returns
    -------
    distances : a list of distances

    """

    distances = []

    for i in range(len(start)):
        x = round(start[i])
        y = round(end[i])

        a = midpoints[x]
        b = midpoints[y]

        distance = math.dist(a, b)
        distances.append(distance)

    return distances


def speed(distances, start, end):
    """
    Calculates the speed of the monkey over a speaker call.
    It takes the distance traveled over a call and
    divides that by the duration of the call

    Parameters
    ----------
    distances : a list of distances

    start : a list of start times

    end : a list of end times

    Returns
    -------
    speeds : a list of speeds per call

    """

    speeds = []
    durations = []

    for i in range(len(start)):
        duration = end[i] - start[i]
        durations.append(duration)

    for j in range(len(distances)):
        speed = distances[j] / durations[j]
        speeds.append(speed)

    return speeds


def pause(midpt, start):
    """
    Determines the average movement of the monkey over a call.
    It finds the distance between the midpoints of the current frame
    and the previous one and determines the average distance traveled.
    It does this for every call.

    Parameters
    ----------
    midpt : a list of midpoints

    start : a list of start times

    end : a list of end times

    Returns
    -------
    mean_distance : a list of average distances traveled

    """

    list_of_temp_distance = []
    temp_distance = []
    mean_distance = []

    for i in range(len(start) - 1):
        x = round(start[i])
        y = round(start[i] + 1)

        a = midpt[x]
        b = midpt[y]
        distance = math.dist(a, b)
        temp_distance.append(distance)

    list_of_temp_distance.append(temp_distance)

    for lst in list_of_temp_distance:
        value = 0
        total = 0

        for dist in lst:
            if not math.isnan(dist):
                value += dist
                total += 1

            avg = value / total
            mean_distance.append(avg)

    return mean_distance
