def review_average_rate(reviews):
    sum_of_average = 0
    if reviews.count() > 0:
        for review in reviews.all():
            sum_of_average += review.average_rate
        try:
            return_value = sum_of_average / reviews.count()
        except ZeroDivisionError:
            return 0

        return round(return_value, 1)
    else:
        return 0


def curriculum_average_rate(reviews):
    curriculum_sum = 0
    if reviews.count() > 0:
        for review in reviews.all():
            curriculum_sum += review.curriculum
        try:
            return_value = curriculum_sum / reviews.count()
        except ZeroDivisionError:
            return 0
        return round(return_value, 1)
    else:
        return 0


def readiness_average_rate(reviews):
    readiness_sum = 0
    if reviews.count() > 0:
        for review in reviews.all():
            readiness_sum += review.readiness
        try:
            return_value = readiness_sum / reviews.count()
        except ZeroDivisionError:
            return 0
        return round(return_value, 1)
    else:
        return 0


def timeliness_average_rate(reviews):
    timeliness_sum = 0
    if reviews.count() > 0:
        for review in reviews.all():
            timeliness_sum += review.timeliness
        try:
            return_value = timeliness_sum / reviews.count()
        except ZeroDivisionError:
            return 0
        return round(return_value, 1)
    else:
        return 0


def delivery_average_rate(reviews):
    delivery_sum = 0
    if reviews.count() > 0:
        for review in reviews.all():
            delivery_sum += review.delivery
        try:
            return_value = delivery_sum / reviews.count()
        except ZeroDivisionError:
            return 0
        return round(return_value, 1)
    else:
        return 0


def friendliness_average_rate(reviews):
    friendliness_sum = 0
    if reviews.count() > 0:
        for review in reviews.all():
            friendliness_sum += review.friendliness
        try:
            return_value = friendliness_sum / reviews.count()
        except ZeroDivisionError:
            return 0
        return round(return_value, 1)
    else:
        return 0
