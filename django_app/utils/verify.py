from member.models import Tutor


def tutor_verify(request, talent):
    """
    1. 요청하는 유저가 튜터인지 확인을 먼저 한 후
    2. 추가하고자 하는 talent의 튜터와 요청하는 유저(튜터)의 정보가 같은지 확인한다.
    """
    tutor_list = Tutor.objects.values_list('user_id', flat=True)
    user = request.user
    if user.id in tutor_list:
        if talent.tutor == user.tutor:
            return True
    return False
