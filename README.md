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
	- [Logout](#logout)
	- [UserDetail](#userdetail)
- Talent
	- [Talent List](#talent-list)

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
  ]
}
```

name 필드에 대한 에러메시지 커스터마이징 필요.

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

---

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
rest-auth에서 자동적으로 Error에 대한 처리를 하지 않기 때문에 커스터마이징 필요


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
  "received_registrations": 0
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

Key|Value
---|---
limit|한 번에 보여줄 아이템 수

> 한 번에 모든 아이템을 반환하려면 limit를 입력하지 않는다.

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

---


# 수정

## 수정사항_001

- 수정 날짜 : 2017. 04. 07.
- 수정 내용 
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
