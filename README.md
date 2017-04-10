# Gori Project API Documentation

굵은 글씨로 표시된 Key는 필수값  
사용자 인증은 Token Authorization을 사용하며, Header의 Authorizationkey에 Token [Token key value]value를 추가하여 이용한다.

## Repository

[https://github.com/lewis810k/gori](https://github.com/lewis810k/gori)

## API Base

`https://mozzi.co.kr/api`

## API 목록
- [Obtain Token](#obtain-token)
- Member
	- [Signup](#signup)
	- [Login](#login)
	- [Facebook Login](#facebook-login)
	- [Logout](#logout)
	- [UserDetail](#userdetail)
- Talent
	- [Talent List](#talent-list)
	- [Talent Detail Retrieve All](#talent-detail-retrieve-all)  
	- . 
	- [Talent Detail Retrieve Fragments](#talent-detail-retrieve-fragments)
	- [Talent Detail Short Retrieve](#talent-detail-short-retrieve)
	- [Talent Location Retrieve](#talent-location-retrieve)
	- [Talent Curriculum Retrieve](#talent-curriculum-retrieve)
	- [Talent Class Image Retrieve](#talent-class-image-retrieve)
	- .
	- [Talent Review Retrieve](#talent-review-retrieve)
	- [Talent Registration Retrieve](#talent-registration-retrieve)

- [수정내용](#수정)

## Obtain Token

### URL

`/member/token-auth/`

### Method

`POST`

### Header

None

### URL Params

None

### Data Params

#### 1. 일반유저

key|Description|Type
---|---|---
**username**|회원가입하는 사용자 이메일|String
**password**|패스워드|String

#### 2. 페이스북 유저
 
key|Value
---|---
**access_token**|Token Key Value

### Success Response
- Code: 201
- Content

Token Key Value

```Json
{
  "key": "3a9fcdcf85afbf783ad5ffed3a3966dc07314acd"
}
```

### Error Response
- Code: 400
	- Reason
		- 필수항목 누락
		- 정보 불일치
	- Content

```Json
{
  "username": [
    "이 항목을 채워주십시오."
  ]
}
```

```Json
{
  "non_field_errors": [
    "제공된 인증데이터(credentials)로는 로그인할 수 없습니다."
  ]
}
```


## Signup

### URL

`/member/signup/`

### Method

`POST`

### Header

None

### URL Params

None

### Data Params

key|Description|Type
---|---|---
**username**|회원가입하는 사용자 이메일|String
**password1**|패스워드|String
**password2**|패스워드 확인용|String
**name**|사용자 이름|String

### Success Response
- Code: 201
- Content

Token Key Value

```Json
{
  "key": "3a9fcdcf85afbf783ad5ffed3a3966dc07314acd"
}
```

### Error Response
- Code: 400
	- Reason
		- 필수항목 누락
		- username 중복
		- password 불일치
	- Content
	 
```Json
{
  "username": [
    "해당 사용자 이름은 이미 존재합니다."
  ]
}
```

```Json
{
  "non_field_errors": [
    "비밀번호가 일치하지 않습니다."
  ]
}
```

```Json
{
  "password2": [
    "이 항목을 채워주십시오."
  ],
  "name": [
    "이 항목을 채워주십시오."
  ]
}
```

---

## Login

### URL

`/member/login/`

### Method

`POST`

### Header

None

### URL Params

None

### Data Params

key|Description|Type
---|---|---
**username**|사용자 이메일|String
**password**|패스워드|String

### Success Response
- Code: 200
- Content

Token Key Value

```Json
{
  "key": "36ddf1824a5c7aaca5977bbe659655566a17fb86f"
}
```

### Error Response
- Code: 400
	- Reason: 인증 실패
	- Content

```Json
{
  "non_field_errors": [
    "제공된 인증데이터(credentials)로는 로그인할 수 없습니다."
  ]
}
```

## Facebook Login

### URL

`/member/fb_login/`

### Method

`POST`

### Header

None

### URL Params

None

### Data Params

Key|Value
---|---
access_token|Token Key Value

### Success Response

- Code: 200
- Content

Token Key Value

```Json
{
  "key": "b8a2ce39a6515dfe26982adbfdb90f59a0c2d653"
}
```

### Error Response
- Code: 400
	- Reason
		- 필수항목 누락
		- 잘못된 토큰 정보
	- Content

```Json
{
  "non_field_errors": [
    "Incorrect input. access_token is required."
  ]
}
```

```Json
{
  "non_field_errors": [
    "Incorrect value"
  ]
}
```

## Logout

> Authenticate Required

### URL

`/member/logout/`

### Method

`POST`

### Header
Key|Value
---|---
Authorization|Token [Token Key Value]

### Url Params

None

### Data Params

None

### Success Response
- Code: 200
- Content

```Json
{
  "detail": "Successfully logged out."
}
```

### Error Response
- Code: 401
	- Reason
		- 만료되었거나 잘못된 토큰
	- Content

```Json
{
  "detail": "토큰이 유효하지 않습니다."
}
```

```Json
{
  "detail": "토큰이 제공되지 않았습니다."
}
```

## User Detail Retrieve

### URL

`/member/profile/user/`

### Method

`GET`

### Header

Key|Value
---|---
Authorization|Token [Token Key Value]

### URL Params

None

### Data Params

None

### Success Response
- Code: 200
- Content

```Json
{
  "pk": 5,
  "user_id": "y.gori",
  "name": "조영나",
  "nickname": "",
  "cellphone": "",
  "user_type": "Django",
  "is_tutor": false,
  "is_staff": true,
  "is_active": true,
  "profile_image": null,
  "joined_date": "2017-04-05T10:04:55.576160Z",
  "last_login": "2017-04-06T09:37:40.312932Z",
  "received_registrations": 0,
  "sent_registrations": 0,
  "wish_list": 0
}
```

### Error Response
- Code: 401
	- Reason: 잘못된 토큰 정보
	- Content

```Json
{
  "detail": "토큰이 유효하지 않습니다."
}
```

---

## Talent List
### URL

`/talent/list/`

### Method

`GET`

### Header

None

### URL Params

| Key      | Value                      |
| -------- | -------------------------- |
| limit    | 한 번에 보여줄 아이템 수             |
| title    | 수업 제목으로 검색                 |
| region   | 지역 필터링 (지역에 해당하는 key값)    |
| category | 카테고리 필터링 (카테고리에 해당하는 key값) |

> - 한 번에 모든 아이템을 반환하려면 limit를 입력하지 않는다.
> - 복수의 params를 적용시 여러 필터링을 거쳐 해당 사항을 모두 만족하는 결과를 반환한다. 

#### Category 

| Key  | Value   |
| ---- | ------- |
| HNB  | 헬스 / 뷰티 |
| LAN  | 외국어     |
| COM  | 컴퓨터     |
| ART  | 미술 / 음악 |
| SPO  | 스포츠     |
| JOB  | 전공 / 취업 |
| HOB  | 이색취미    |
| ETC  | 기타      |

#### Region 

| Key  | Value |
| ---- | ----- |
| KOU  | 고려대   |
| SNU  | 서울대   |
| YOU  | 연세대   |
| HOU  | 홍익대   |
| EWWU | 이화여대  |
| BSU  | 부산대   |
| JAU  | 중앙대   |
| GGU  | 건국대   |
| HYU  | 한양대   |
| KN   | 강남    |
| SC   | 신촌    |
| SD   | 사당    |
| JS   | 잠실    |
| JR   | 종로    |
| HH   | 혜화    |
| YS   | 용산    |
| HJ   | 합정    |
| MD   | 목동    |
| ETC  | 기타    |


### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "count": 5,
  "next": "http://mozzi.co.kr/api/talent/list/?limit=2&offset=2",
  "previous": null,
  "results": [
    {
      "pk": 2,
      "title": "4주만 몸짱을 만들어 드립니다~",
      "category": "스포츠",
      "type": "그룹 수업",
      "tutor": {
        "pk": 8,
        "user_id": "suji@gmail.com",
        "name": "박수지",
        "nickname": "건강지킴이",
        "is_verified": true,
        "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/%E1%84%8B%E1%85%A8%E1%84%8C%E1%85%A5%E1%86%BC%E1%84%92%E1%85%AA.jpeg",
        "cellphone": ""
      },
      "is_school": false,
      "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/%E1%84%92%E1%85%A2%E1%86%AF%E1%84%89%E1%85%B3.jpeg",
      "price_per_hour": 12000,
      "hours_per_class": 1,
      "number_of_class": 8,
      "is_soldout": false,
      "created_date": "2017-04-05T11:29:52.728809Z",
      "average_rate": 0,
      "review_count": 0,
      "registration_count": 0,
      "regions": [
        "종로"
      ]
    },
    {
      "pk": 3,
      "title": "C언어 어려워도 쉽게 가르쳐드려요",
      "category": "컴퓨터",
      "type": "1:1 수업",
      "tutor": {
        "pk": 10,
        "user_id": "jisungpark@naver.com",
        "name": "박지성",
        "nickname": "컴신",
        "is_verified": true,
        "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/jisung.jpeg",
        "cellphone": "01056463664"
      },
      "is_school": true,
      "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/%E1%84%8A%E1%85%B5%E1%84%8B%E1%85%A5%E1%86%AB%E1%84%8B%E1%85%A5.png",
      "price_per_hour": 12000,
      "hours_per_class": 2,
      "number_of_class": 8,
      "is_soldout": false,
      "created_date": "2017-04-05T11:57:21.278516Z",
      "average_rate": 0,
      "review_count": 0,
      "registration_count": 0,
      "regions": [
        "홍익대",
        "용산"
      ]
    }
  ]
}
```

## Talent Detail Retrieve All

> talent의 기본정보에서 location, curriculum, class_image가 포함되어있다.

### URL

`/talent/detail-all/<talent_pk>/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "pk": 1,
  "title": "네일 고수가 되실 수 있어요",
  "tutor": {
    "pk": 6,
    "user_id": "yuna@gmail.com",
    "name": "김유나",
    "nickname": "유나짱",
    "is_verified": true,
    "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/nail.jpeg",
    "cellphone": "01073858237"
  },
  "category": "헬스 / 뷰티",
  "type": "1:1 수업",
  "average_rate": 0,
  "review_count": 0,
  "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/02.jpeg",
  "tutor_info": "경력 10년차 배테랑입니다",
  "class_info": "다양한 네일 아트 기술을 배우실 수 있어요",
  "video1": "",
  "video2": "",
  "locations": [
    {
      "region": "강남",
      "specific_location": "협의 후 결정",
      "day": "월",
      "extra_fee": "Y",
      "extra_fee_amount": "3만원",
      "time": [
        "14:00-18:00"
      ]
    },
    {
      "region": "신촌",
      "specific_location": "협의 후 결정",
      "day": "화",
      "extra_fee": "N",
      "extra_fee_amount": "",
      "time": [
        "16:00-22:00"
      ]
    }
  ],
  "price_per_hour": 13000,
  "hours_per_class": 2,
  "number_of_class": 4,
  "is_soldout": false,
  "class_images": [
    {
      "image": "https://projectgori.s3.amazonaws.com/media/talent/extra_images/14597239_1856403567907243_4624578483752796160_n.jpg"
    }
  ],
  "curriculums": [
    {
      "information": "1주차는 간단한 풀컬러 네일 수업입니다",
      "image": null
    },
    {
      "information": "2주차는 프렌치 네일",
      "image": null
    },
    {
      "information": "3주차는 젤네일",
      "image": null
    },
    {
      "information": "4주차는 다양한 네일 아트(파티클 붙이기 등)",
      "image": null
    }
  ]
}
```

### Error Response

- Code: 404
  - Reason: Invalid Talent pk
  - Content

```Json
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Detail Retrieve Fragments

## Talent Detail Short Retrieve

### URL

`/talent/detail/<talent_pk>/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "pk": 3,
  "title": "C언어 어려워도 쉽게 가르쳐드려요",
  "tutor": {
    "pk": 10,
    "user_id": "jisungpark@naver.com",
    "name": "박지성",
    "nickname": "컴신",
    "is_verified": true,
    "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/jisung.jpeg",
    "cellphone": "01056463664"
  },
  "category": "컴퓨터",
  "type": "1:1 수업",
  "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/%E1%84%8A%E1%85%B5%E1%84%8B%E1%85%A5%E1%86%AB%E1%84%8B%E1%85%A5.png",
  "tutor_info": "컴공 마스터입니다",
  "class_info": "c 언어의 기초부터 차근차근 가르쳐드리겠습니다. 교재 따로 필요없이 제가 준비해가는 자료를 기반으로 배우시게 됩니다.",
  "average_rate": 3.6,
  "review_count": 0,
  "video1": "",
  "video2": "",
  "price_per_hour": 12000,
  "hours_per_class": 2,
  "number_of_class": 8,
  "is_soldout": false
}
```

### Error Response

- Code: 404
  - Reason: Invalid Talent pk
  - Content

```Json
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Location Retrieve

### URL

`/talent/detail/<talent_pk>/location/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "pk": 1,
  "title": "네일 고수가 되실 수 있어요",
  "category": "헬스 / 뷰티",
  "type": "1:1 수업",
  "locations": [
    {
      "region": "강남",
      "specific_location": "협의 후 결정",
      "day": "월",
      "extra_fee": "Y",
      "extra_fee_amount": "3만원",
      "time": [
        "14:00-18:00"
      ]
    },
    {
      "region": "신촌",
      "specific_location": "협의 후 결정",
      "day": "화",
      "extra_fee": "N",
      "extra_fee_amount": "",
      "time": [
        "16:00-22:00"
      ]
    }
  ]
}
```

### Error Response

- Code: 404
  - Reason: Invalid Talent pk
  - Content

```Json
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Curriculum Retrieve

### URL

`/talent/detail/<talent_pk>/curriculum/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "pk": 1,
  "title": "네일 고수가 되실 수 있어요",
  "category": "헬스 / 뷰티",
  "type": "1:1 수업",
  "curriculums": [
    {
      "information": "1주차는 간단한 풀컬러 네일 수업입니다",
      "image": "https://projectgori.s3.amazonaws.com/media/talent/curriculum/KakaoTalk_Photo_2017-03-29-23-05-12_76.jpeg"
    },
    {
      "information": "2주차는 프렌치 네일",
      "image": null
    },
    {
      "information": "3주차는 젤네일",
      "image": null
    },
    {
      "information": "4주차는 다양한 네일 아트(파티클 붙이기 등)",
      "image": null
    }
  ]
}
```

### Error Response

- Code: 404
  - Reason: Invalid Talent pk
  - Content

```Json
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Class Image Retrieve

### URL

`/talent/detail/<talent_pk>/class-image/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "pk": 1,
  "title": "네일 고수가 되실 수 있어요",
  "category": "헬스 / 뷰티",
  "type": "1:1 수업",
  "class_images": [
    {
      "image": "https://projectgori.s3.amazonaws.com/media/talent/extra_images/%E1%84%91%E1%85%B3%E1%84%85%E1%85%A6%E1%86%AB%E1%84%8E%E1%85%B5_%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF.jpg"
    }
  ]
}
```

### Error Response

- Code: 404
  - Reason: Invalid Talent pk
  - Content

```Json
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Review Retrieve

### URL

`talent/detail/<talent_pk>/review/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```
{
  "pk": 4,
  "title": "봉쥬르~불어 어렵지 않아요~",
  "category": "외국어",
  "type": "1:1 수업",
  "average_rate": 3.6,
  "review_count": 1,
  "reviews": [
    {
      "pk": 1,
      "talent": "봉쥬르~불어 어렵지 않아요~",
      "user": {
        "pk": 9,
        "name": "최소진",
        "profile_image": null
      },
      "curriculum": 3,
      "readiness": 2,
      "timeliness": 4,
      "delivery": 4,
      "friendliness": 5,
      "created_date": "2017-04-07T12:19:45.725675Z",
      "comment": ""
    }
  ]
}
```

### Error Response
- Code: 404
	- Reason: Invalid Talent pk
	- Content

```
{
  "detail": "찾을 수 없습니다."
}
```

## Talent Registration Retrieve

### URL

`talent/detail/<talent_pk>/registration/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

```
{
  "pk": 3,
  "title": "C언어 어려워도 쉽게 가르쳐드려요",
  "category": "컴퓨터",
  "type": "1:1 수업",
  "registrations": [
    {
      "pk": 1,
      "name": "a.gori",
      "talent_location": "홍익대",
      "student_level": "입문자",
      "experience_length": 3,
      "is_confirmed": false,
      "joined_date": "2017-04-09T06:44:44.335378Z",
      "message_to_tutor": "초보자입니다. 잘 부탁드립니다."
    }
  ]
}
```

### Error Response
- Code: 404
	- Reason: Invalid Talent pk
	- Content

```
{
  "detail": "찾을 수 없습니다."
}
```



# 수정

## 수정사항_002

- 수정 날짜 : 2017. 04. 10.
- 주요 내용 
	- API 추가
		- Facebook Login 
		- Talent Detail Retrieve All 
		- Talent Detail Retrieve Fragments 
		- Talent Detail Short Retrieve 
		- Talent Location Retrieve 
		- Talent Curriculum Retrieve 
		- Talent Class Image Retrieve 
		- Talent Review Retrieve 
		- Talent Registration Retrieve 
	- API 수정

### # API 수정 내용

### Login

- Method 변경 : `GET` -> `POST`
- Params 변경 : `Url Params` -> `Data Params`

### Logout

- Error Response 추가

### Signup

- Custom 필드에 대한 Error Response 추가

### User Detail Retrieve

- 필드 추가 

Field|Description|Type
---|---|---
sent_registrations|보낸 신청서 수|Int
wish_list|위시리스트 수업 수|Int

### Talent List

- 검색, 필터링에 대한 Url Params 추가

Field|Description|Type
---|---|---
| title    | 수업 제목으로 검색                 |String
| region   | 지역 필터링 (지역에 해당하는 key값)    |String
| category | 카테고리 필터링 (카테고리에 해당하는 key값) |String


## 수정사항_001

- 수정 날짜 : 2017. 04. 07.
- 주요 내용 
	- 문서 제목 추가
	- API 수정

### # API 수정 내용

### User Detail Retrieve

- 필드 순서 재배치
- 필드 추가 

Field|Description|Type
---|---|---
nickname|닉네임|String
received_registrations|받은 수업 신청서 수|Int


### Talent List

- 필드 순서 재배치
- 필드 추가

Field|Description|Type
---|---|---
is_school|장소에 캠퍼스가 속해있는지|Bool
average_rate|평점|Float
registration_count|받은 신청서 수|Int

- 필드명 변경

Old Name|New Name
---|---
type_name | type
category_name | category
locations | regions
