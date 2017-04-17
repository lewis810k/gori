from talent.models import Location


def region_display(region):
    for item in Location.SCHOOL+Location.AREA:
        if item[0] == region:
            return item[1]