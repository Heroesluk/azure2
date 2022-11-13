def check_black_amount(c1):
    # 0-255 - > 0-100
    brightness = c1[2]/2.55

    if brightness < 25:
        if brightness == 0:
            brightness = 1

        return 1

    return 0



def check_gray_scale(c1,low,high):
    # 0-255 - > 0-100
    saturation = c1[1]*100
    brightness = c1[2]/2.55


    if (saturation < 4) and (high>brightness>low):
        return 1

    return 0

def check_if_close_color(c1, c2):
    hue1, hue2 = c1[0] * 359, c2[0] * 359
    # if abs(hue1-hue2)<50:
    # print(c2,c1,'value', (abs(hue1-hue2)<50),c1[1],(c1[2]/255))
    distance = abs(hue1 - hue2)
    if distance < 25:
        if distance == 0:
            multiplier = 1
        else:
            multiplier = 1

        return multiplier * c2[1] * (c2[2] / 255)

    return 0


def check_white_amount(c1):
    # 0-1
    saturation = c1[1]*100
    brightness = c1[2]/2.55

    if saturation < 2 and brightness>99:
        return 1

    return 0