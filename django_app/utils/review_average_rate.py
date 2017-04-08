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
