# 동아리 플랫폼 백엔드 API 문서

## API 엔드포인트 목록

### 1. 인증 API (`/api/auth`)

#### `POST /api/auth/register`
- **기능**: 신규 학생 회원가입
- **인증**: 불필요
- **요청 본문**: 
  ```json
  {
    "Student_ID": "string",
    "Login_ID": "string",
    "Pw": "string",
    "Name": "string",
    "phone_num": "string (optional)",
    "Email": "string (optional)"
  }
  ```
- **응답**: 201 Created (성공), 400 Bad Request, 409 Conflict

#### `POST /api/auth/login`
- **기능**: 학생 로그인 및 JWT 토큰 발급
- **인증**: 불필요
- **요청 본문**: 
  ```json
  {
    "Login_ID": "string",
    "Pw": "string"
  }
  ```
- **응답**: 200 OK (토큰 포함), 400 Bad Request, 401 Unauthorized

---

### 2. 동아리 API (`/api/club`)

#### `GET /api/club`
- **기능**: 동아리 전체 목록 조회 (공개)
- **인증**: 불필요
- **쿼리 파라미터**: `category` (optional) - 카테고리별 필터링
- **응답**: 200 OK (동아리 목록), 500 Internal Server Error

#### `GET /api/club/<club_id>`
- **기능**: 동아리 상세 정보 조회 (공개)
- **인증**: 불필요
- **응답**: 200 OK (동아리 상세 정보), 404 Not Found

#### `PUT /api/club/<club_id>`
- **기능**: 동아리 정보 수정 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Club_Introduction": "string (optional)",
    "Category": "string (optional)"
  }
  ```
- **응답**: 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

#### `GET /api/club/<club_id>/members`
- **기능**: 동아리 회원 목록 조회 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK (회원 목록), 403 Forbidden, 404 Not Found

#### `DELETE /api/club/member/<membership_id>`
- **기능**: 동아리 회원 강퇴 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK, 403 Forbidden, 404 Not Found

---

### 3. 가입 신청 API (`/api/apply`)

#### `POST /api/apply/<club_id>`
- **기능**: 동아리 가입 신청 (학생)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Self_Introduction": "string (optional)"
  }
  ```
- **응답**: 201 Created, 409 Conflict, 500 Internal Server Error

#### `GET /api/apply/manage/<club_id>`
- **기능**: 동아리 신청 목록 조회 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK (신청 목록), 403 Forbidden, 404 Not Found

#### `PUT /api/apply/manage/<application_id>`
- **기능**: 신청서 상태 변경 (승인/거절) (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Status": "승인" 또는 "거절"
  }
  ```
- **응답**: 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### 4. 게시글 API

#### `GET /api/club/<club_id>/post`
- **기능**: 특정 동아리 게시글 목록 조회 (공개)
- **인증**: 불필요
- **응답**: 200 OK (게시글 목록), 500 Internal Server Error

#### `POST /api/club/<club_id>/post`
- **기능**: 특정 동아리 게시글 작성 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Content": "string"
  }
  ```
- **응답**: 201 Created, 400 Bad Request, 403 Forbidden, 404 Not Found

#### `PUT /api/post/<post_id>`
- **기능**: 게시글 수정 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Content": "string"
  }
  ```
- **응답**: 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

#### `DELETE /api/post/<post_id>`
- **기능**: 게시글 삭제 (관리자 전용)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK, 403 Forbidden, 404 Not Found

---

### 5. 마이페이지 API (`/api/mypage`)

#### `GET /api/mypage/info`
- **기능**: 내 정보 조회 (로그인 필수)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK (사용자 정보), 404 Not Found

#### `PUT /api/mypage/info`
- **기능**: 내 정보 수정 (로그인 필수)
- **인증**: 필요 (JWT 토큰)
- **요청 본문**: 
  ```json
  {
    "Name": "string (optional)",
    "phone_num": "string (optional)",
    "Email": "string (optional)",
    "Pw": "string (optional)"
  }
  ```
- **응답**: 200 OK, 400 Bad Request, 409 Conflict

#### `GET /api/mypage/applications`
- **기능**: 내 가입 신청 현황 조회 (로그인 필수)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK (신청 목록), 500 Internal Server Error

#### `GET /api/mypage/clubs`
- **기능**: 내가 가입한 동아리 목록 조회 (로그인 필수)
- **인증**: 필요 (JWT 토큰)
- **응답**: 200 OK (동아리 목록), 500 Internal Server Error

---

### 6. 관리자 API (`/api/admin`)

#### `GET /api/admin/stats`
- **기능**: 사이트 전체 통계 조회 (사이트 관리자 전용)
- **인증**: 필요 (JWT 토큰, Role='관리자')
- **응답**: 200 OK (통계 정보), 403 Forbidden, 500 Internal Server Error

---

## 인증 방식

대부분의 API는 JWT 토큰 기반 인증을 사용합니다.

**헤더 형식**:
```
Authorization: Bearer <JWT_TOKEN>
```

로그인 API(`POST /api/auth/login`)를 통해 토큰을 발급받아 사용합니다.

---

## 권한 구분

- **공개**: 인증 없이 접근 가능
- **학생**: 로그인한 모든 학생 접근 가능
- **관리자**: 해당 동아리의 관리자만 접근 가능
- **사이트 관리자**: Role이 '관리자'인 사용자만 접근 가능

