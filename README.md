# Wanted: 프리온보딩 백엔드 코스 4차 선발과제
- 본 서비스는 기업의 채용을 위한 웹 서비스 입니다.
- 회사는 채용공고를 생성하고, 이에 사용자는 지원합니다.
## 🛠 사용 기술
- Django
- MySQL

## 📚 모델링
![wanted](https://user-images.githubusercontent.com/93898332/185731370-38f5c85f-7ebe-4029-8e06-1b0f119c1816.png)

## 🔖 구현사항
### 0. 기업/일반회원 가입 및 로그인
#### -URL
- POST `/companies/signup`
- GET `/companies/signin`
- POST `/users/signup`
- GET `/users/signin`

#### 기능
- 기업
    - 등록 조건: 비밀번호 4자리 이상이고, 기업 이름이 중복되지 않을 것.
    - 비밀번호는 암호화되어 데이터베이스에 저장.
    - 기업 이름과 비밀번호를 입력하면 토큰 발행.

- 일반회원
    - 등록 조건: 비밀번호 4자리 이상이고, 이메일이 중복되지 않을 것.
    - 비밀번호는 암호화되어 데이터베이스에 저장.
    - 이메일과 비밀번호를 입력하면 토큰 발행.
### 1. 채용공고 등록
#### URL
- POST `/companies/post`

#### 기능
- 등록 조건: 로그인을 해야하고, 해당 기업이 아니면 등록되지 않음.

### 2. 채용공고 수정
#### URL
- PATCH `/companies/update/:announcement_id`

#### 기능
- 수정 조건: 로그인을 해야하고, 해당 기업이 아니면 수정되지 않음.
- 회사 id 외 수정 가능

### 3. 채용공고 삭제
#### URL
- DELETE `/companies/delete/:announcement_id`

#### 기능
- 삭제 조건: 로그인을 해야하고, 해당 기업이 아니면 삭제되지 않음.

### 4. 채용공고 목록 확인
#### URL
- GET `/companies/get`

#### 예시
```
{
    "results": [
        {
            "announcement_id": 1,
            "company": "원티드랩",
            "title": "백엔드 주니어 개발자 모집",
            "content": "원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "position": "백엔드 주니어 개발자",
            "compensation": 1500000,
            "skill": "Python"
        }
    ]
}
```
### 5. 채용공고 검색 기능
#### URL
- GET `/companies/get?search=`

#### 기능
- 회사명, 채용포지션, 채용스킬에 검색 내용이 포함된 채용 공고만 조회.

### 6. 채용 상세페이지
#### URL
- GET `/companies`

#### 기능
- 해당 회사가 올린 다른 채용공고 가 추가적으로 포함됨.

#### 예시
```
{
    "results": [
        {
            "announcement_id": 10,
            "company": "원티드랩",
            "title": "백엔드 주니어 개발자 모집",
            "content": "네이버에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "position": "백엔드 주니어 개발자",
            "compensation": 2000000,
            "skill": "Python",
            "other announcement_id": [
                1,
                10
            ]
        }
    ]
}
```

### 7. 채용공고 지원
#### URL
- POST `/users/:announcement_id`

#### 기능
- 로그인을 후 채용 공고 지원 가능.
- 이미 지원한 상태에 다시 지원하면 삭제가 됨.

## 💻 AIP 명세서: Postman
https://documenter.getpostman.com/view/18832289/VUqoSKEp
