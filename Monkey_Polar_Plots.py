import math
import matplotlib.pyplot as plt
import numpy as np


def clean(list):
    """
    This function cleans the given list by taking out all the nan's'

    Parameters
    ----------
    list : a list of circular means.

    Returns
    -------
    cleaned : the same list but without the 'nan's.

    """
    cleaned = [x for x in list if str(x) != "nan"]
    # to be in line with the plot
    cleaned = [value + 180 + 90 for value in cleaned]
    cleaned = [value - 360 if value > 360 else value for value in cleaned]

    return cleaned


def get_cleaned_data(raw_data, raw_speaker, speaker_num):
    organized = organize(raw_data)
    temp = calculate_angle(organized)
    fixed_angles = fix_angles(temp)

    calls = []

    for call in raw_speaker:
        if call[2] == speaker_num:
            calls.append(call)

    start_lst = start(calls)
    end_lst = end(calls)

    circ_means = circular_mean(fixed_angles, start_lst, end_lst)
    cleaned_data = clean(circ_means)

    return cleaned_data


def fix_angles(angles):
    fixed_angles = []

    for angle in angles:
        if angle <= 90:
            angle = 90 - angle

        elif angle <= 180:
            angle = 90 - (angle - 90) + 90

        elif angle <= 270:
            angle = 90 - (angle - 180) + 180

        else:
            angle = 90 - (angle - 270) + 270

        fixed_angles.append(angle)

    return fixed_angles


def organize(data_lst):
    """
    This function iterates through the raw 3d list and extracts the
    x and y coordinates of each point (2 ear points and a nose point)
    within each frame (labeled frame from sleap)

    Parameters
    ----------
    data_lst : a raw data list

    Returns
    -------
    frame_list : the x and y coordinates of each point

    """

    frame_list = []

    for frame in data_lst:
        point_list = []
        frame_list.append(point_list)

        for point in frame:
            coord_list = []
            point_list.append(coord_list)

            for coord in point:
                coord_list.append(coord)

    return frame_list


def calculate_angle(pts):
    """
    This function takes a list of data points and calculates
    the slope between the average ear coordinate and the nose. Then
    it calculates the angle in degrees of that slope with respect to a
    straight line. Then, if the rise of the "rise/run" for each slope was positive,
    it adds 180 degrees to that angle. Finally, it adds the adjusted angles to a list.

    Parameters
    ----------
    pts : a list of x/y coordinates.

    Returns
    -------
    adjusted_angles : a list of angles that
    range the full 360 degrees

    """

    angles = []
    adjusted_angles = []

    for line in pts:
        avg_ear_x = (line[0][0] + line[1][0]) / 2
        avg_ear_y = (line[0][1] + line[1][1]) / 2
        avg_ear_coord = [avg_ear_x, avg_ear_y]

        rise = (line[1][1]) - (avg_ear_coord[1])

        run = (line[1][0]) - (avg_ear_coord[0])

        slope = rise / run
        angle_radians = math.atan(slope)
        angle_degrees = math.degrees(angle_radians)

        if rise > 0:
            angle_degrees += 180

        angles.append(angle_degrees)

    adjusted_angles = [angle + 90 for angle in angles]

    return adjusted_angles


def start(target_lst):
    """
    This function adds the start time of each call to a list

    Parameters
    ----------
    target_lst : a list of target calls in the form of
    start time, end time

    Returns
    -------
    starts : a list of start times

    """

    starts = []

    for time in target_lst:
        starts.append(time[0])

    return starts


def end(target_lst):
    """
    This function adds the end time of each call

    Parameters
    ----------
    target_lst : a list of target calls in the form of
    start time, end time

    Returns
    -------
    ends : a list of end times

    """

    ends = []

    for time in target_lst:
        ends.append(time[1])

    return ends


def circular_mean(angle_lst, list_start, list_end):
    """
    This function adds the angles for a call
    (the angles in between that call's start and end time) to a
    temporary list. Then, it calculates the circular mean of those angles
    (in degrees) within the temporary list. It does this for every call.

    Parameters
    ----------
    angle_lst : A list of angles
    list_start : A list of start times
    list_end : A list of end times

    Returns
    -------
    circular_means : A list of circular means

    """

    circular_means = []
    for_calculation = []

    # adds each angle for the frames during the target call to a temporary list
    # then adds that list of angles to a larger list for circular mean calculation
    for i in range(len(list_start)):
        x = round(list_start[i])
        y = round(list_end[i])
        temp = []

        for angle in angle_lst[x:y]:
            temp.append(angle)

        for_calculation.append(temp)

    # circular mean for angles in for_calculation using np.arctan2, np.sines. np.cosines

    for angles in for_calculation:
        sines = np.sin(np.deg2rad(angles))
        cosines = np.cos(np.deg2rad(angles))
        circular_mean_rads = np.arctan2(np.nansum(sines), np.nansum(cosines))
        circular_mean_degs = np.rad2deg(circular_mean_rads)

        # add that circular mean to the list
        circular_means.append(circular_mean_degs)

    return circular_means


nbins = 12
edges = np.linspace(0, 360, nbins + 1)
bins = np.deg2rad(edges[:-1] + 360 / (2 * nbins))

ax = plt.subplot(131, projection="polar")
speaker4_bars = np.histogram(s4_data, edges)
bars = ax.bar(bins, speaker4_bars[0], color="magenta", width=2 * np.pi / len(bins))
ax.set_title("Speaker 4")

ax = plt.subplot(132, projection="polar")
speaker5_bars = np.histogram(s5_data, edges)
bars = ax.bar(bins, speaker5_bars[0], color="blue", width=2 * np.pi / len(bins))
ax.set_title("Speaker 5")

ax = plt.subplot(133, projection="polar")
speaker6_bars = np.histogram(s6_data, edges)
bars = ax.bar(bins, speaker6_bars[0], color="black", width=2 * np.pi / len(bins))
ax.set_title("Speaker 6")
plt.show()

all_speaker_bars[f, 0, :] = speaker4_bars[0] / np.nansum(speaker4_bars[0])
all_speaker_bars[f, 1, :] = speaker5_bars[0] / np.nansum(speaker5_bars[0])
all_speaker_bars[f, 2, :] = speaker6_bars[0] / np.nansum(speaker6_bars[0])

# Plot the average across all monkeys
ax = plt.subplot(131, projection="polar")
bars = ax.bar(
    bins,
    np.nanmean(all_speaker_bars[:, 0, :], axis=0),
    color="magenta",
    width=2 * np.pi / len(bins),
)
ax.set_title("Speaker 4")
ax.set_ylim((0, 0.15))

ax = plt.subplot(132, projection="polar")
bars = ax.bar(
    bins,
    np.nanmean(all_speaker_bars[:, 1, :], axis=0),
    color="blue",
    width=2 * np.pi / len(bins),
)
ax.set_title("Speaker 5")
ax.set_ylim((0, 0.15))

ax = plt.subplot(133, projection="polar")
bars = ax.bar(
    bins,
    np.nanmean(all_speaker_bars[:, 2, :], axis=0),
    color="black",
    width=2 * np.pi / len(bins),
)
ax.set_title("Speaker 6")
ax.set_ylim((0, 0.15))
plt.show()
