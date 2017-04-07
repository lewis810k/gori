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

`GET`

### Header

None

### URL Params

key|Description|Type
---|---|---
**username**|사용자 이메일|String
**password**|패스워드|String

### Data Params

None

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
  "pk": 2,
  "user_id": "admin",
  "name": "어드민",
  "user_type": "Django",
  "is_staff": true,
  "is_active": true,
  "cellphone": "01012345678",
  "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/article.jpg",
  "joined_date": "2017-03-30T08:45:41.606558Z",
  "is_tutor": false,
  "last_login": "2017-04-04T09:09:25Z"
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
limit|한 번에 보여줄 아이템 갯수

> 한 번에 모든 아이템을 반환하려면 limit를 입력하지 않는다.

### Data Params

None

### Success Response

- Code: 200
- Content

```Json
{
  "count": 5,
  "next": "http://localhost:8000/api/talent/list/?limit=3&offset=3",
  "previous": null,
  "results": [
    {
      "pk": 1,
      "tutor": {
        "pk": 2,
        "user_id": "admin",
        "name": "어드민",
        "nickname": "",
        "is_verified": false,
        "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/article.jpg",
        "cellphone": "01012345678"
      },
      "title": "파이썬 장고",
      "category_name": "컴퓨터",
      "type_name": "그룹 수업",
      "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/article.jpg",
      "price_per_hour": 1,
      "hours_per_class": 1,
      "number_of_class": 1,
      "is_soldout": false,
      "created_date": "2017-03-31T08:51:55.257701Z",
      "review_count": 0,
      "locations": [
        "강남",
        "종로"
      ]
    },
    {
      "pk": 2,
      "tutor": {
        "pk": 2,
        "user_id": "admin",
        "name": "어드민",
        "nickname": "",
        "is_verified": false,
        "profile_image": "https://projectgori.s3.amazonaws.com/media/member/profile_image/article.jpg",
        "cellphone": "01012345678"
      },
      "title": "영화보자",
      "category_name": "미술 / 음악",
      "type_name": "원데이 수업",
      "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/beuxnVcF.jpg",
      "price_per_hour": 1,
      "hours_per_class": 1,
      "number_of_class": 1,
      "is_soldout": false,
      "created_date": "2017-03-31T08:58:01.770976Z",
      "review_count": 0,
      "locations": [
        "사당"
      ]
    },
    {
      "pk": 3,
      "tutor": {
        "pk": 89,
        "user_id": "test_api@gmail.com",
        "name": "lewis",
        "nickname": "",
        "is_verified": true,
        "profile_image": null,
        "cellphone": ""
      },
      "title": "바리스타 마스터 코스",
      "category_name": "이색취미",
      "type_name": "그룹 수업",
      "cover_image": "https://projectgori.s3.amazonaws.com/media/talent/cover_image/article_rEC7reP.jpg",
      "price_per_hour": 10,
      "hours_per_class": 2,
      "number_of_class": 8,
      "is_soldout": false,
      "created_date": "2017-04-05T05:47:04.488888Z",
      "review_count": 2,
      "locations": [
        "신촌",
        "사당"
      ]
    }
  ]
}
```

