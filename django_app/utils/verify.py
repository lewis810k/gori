from member.models import Tutor
from talent.models import Talent


def verify_tutor(request, model):
    """
    1. 요청하는 유저가 튜터인지 확인을 먼저 한 후
    2. 추가하고자 하는 talent의 튜터와 요청하는 유저(튜터)의 정보가 같은지 확인한다.
    """
    tutor_list = Tutor.objects.values_list('user_id', flat=True)
    user = request.user
    if user.id in tutor_list:
        if model.tutor == user.tutor:
            return True
    return False


def verify_duplicate(model, data):
    """
    특정 모델을 넘겨 받아 해당 data으로 구성된 아이템이 존재하는지 체크
    :param model: 중복체크하고자 하는 모델
    :param data:
    :return:
    """
    ret = {
        'detail': '이미 존재하는 항목입니다.'
    }
    if model.objects.filter(**data).count() > 0:
        return True, ret
    else:
        return False, {}


def verify_instance(model, pk):
    instance = model.objects.get(pk=pk)
    if instance.is_verified:
        instance.is_verified = False
        detail = "[{}] 인증 취소되었습니다.".format(instance)
    else:
        instance.is_verified = True
        detail = "[{}] 인증 되었습니다.".format(instance)
    instance.save()
    return instance, detail


def verify_data(data, type):
    """
    post 요청으로 넘겨받은 데이터의 유효성을 점검한다.
    A. 빈 값 체크
    B. 숫자형태 체크

    type == 1 : A, B
    type == 2 : A

    :param data: response.data
    :param type: 검증 형태
    :return:
    """
    if type == 1:
        for key, value in data.items():
            if value.strip() == '':
                return False
            if not value.isdigit():
                return False
    if type == 2:
        for key, value in data.items():
            if value.strip() == '':
                return False
    return True

def switch_sales_status(pk):
    talent = Talent.objects.get(pk=pk)
    if talent.is_soldout:
        talent.is_soldout = False
        detail = "수업이 [{}] SOLD OUT 취소되었습니다.".format(talent.title)
    else:
        talent.is_soldout = True
        detail = "수업이 [{}] SOLD OUT 되었습니다.".format(talent.title)
    talent.save()
    return talent, detail
