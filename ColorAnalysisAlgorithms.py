import math


def check_black_amount(c1):
    # 0-255 - > 0-100
    brightness = c1[2]/2.55

    if brightness < 25:
        if brightness == 0:
            brightness = 1

        return 1

    return 0


#not completed
def check_gray_scale(c1,low,high):
    # 0-255 - > 0-100
    saturation = c1[1]*100
    brightness = c1[2]/2.55


    if (saturation < 4) and (high>brightness>low):
        return 1

    return 0

def check_if_close_color(c1, c2):
    hue1, hue2 = c1[0] * 359, c2[0] * 359

    #print(hue2, hue2==359, hue2==359.0)

    saturation = c1[1]*100
    brightness = c1[2]/2.55

    # if abs(hue1-hue2)<50:
    # print(c2,c1,'value', (abs(hue1-hue2)<50),c1[1],(c1[2]/255))
    distance = abs(hue1 - hue2)
    #print(distance)
    if distance < 25 and saturation>5 and brightness>30:
        if distance == 0:
            multiplier = 1
        else:
            multiplier = (1/distance)*saturation

        return multiplier

    elif hue2==0.0 and distance>340 and saturation>5 and brightness>30:
        distance = 360-distance
        return (1/distance)*math.sqrt(saturation)


    return 0


def check_white_amount(c1):
    # 0-1
    saturation = c1[1]*100
    brightness = c1[2]/2.55

    if saturation < 2 and brightness>99:
        return 1

    return 0


