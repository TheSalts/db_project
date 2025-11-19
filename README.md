# 동아리 플랫폼

학생들을 위한 종합 동아리 관리 플랫폼입니다. 동아리 탐색, 가입 신청, 회원 관리, 게시글 작성 등의 기능을 제공합니다.

## 프로젝트 구조

```
db_project/
├── server/          # Flask 백엔드 (Python)
│   ├── app/
│   │   ├── api/     # API 엔드포인트
│   │   ├── services/ # 비즈니스 로직
│   │   └── utils/   # 유틸리티 (DB, 인증)
│   ├── run.py       # 서버 실행 파일
│   └── README.md    # 백엔드 문서
│
└── client/          # React 프론트엔드 (TypeScript)
    ├── src/
    │   ├── components/ # 공통 컴포넌트
    │   ├── pages/      # 페이지
    │   ├── contexts/   # React Context
    │   ├── services/   # API 서비스
    │   └── types/      # 타입 정의
    └── README.md    # 프론트엔드 문서
```

## 기술 스택

### 백엔드
- **Flask** - Python 웹 프레임워크
- **PyMySQL** - MySQL 데이터베이스 연결
- **JWT** - 인증 토큰
- **bcrypt** - 비밀번호 해싱

### 프론트엔드
- **React 18** + **TypeScript**
- **Vite** - 빌드 도구
- **React Router** - 라우팅
- **Axios** - HTTP 클라이언트

### 데이터베이스
- **MySQL** - 관계형 데이터베이스

## 주요 기능

### 1. 메인 페이지
- 회원가입, 로그인, 로그아웃
- 전체 동아리 목록 조회
- 카테고리별 필터링
- 동아리 상세 정보 확인
- 동아리 가입 신청

### 2. 학생 기능 (마이페이지)
- 개인 정보 수정
- 가입한 동아리 목록
- 가입 신청 현황 확인 (대기/승인/거절)

### 3. 동아리 관리자 기능
- 동아리 정보 수정
- 게시글 작성/수정/삭제
- 가입 신청 승인/거절
- 회원 목록 조회 및 강퇴

### 4. 사이트 관리자 기능
- 전체 통계 대시보드
  - 전체 학생 수
  - 전체 동아리 수
  - 대기 중인 신청
  - 카테고리별 동아리 현황
- 새 동아리 생성

## 실행 방법

### 🚀 빠른 시작 (자동 설정)

**macOS/Linux:**
```bash
./setup.sh
```

이 스크립트가 자동으로:
1. .env 파일 체크
2. Python 가상환경 생성
3. 패키지 설치
4. 데이터베이스 초기화
5. 프론트엔드 패키지 설치

**Windows:**
수동으로 아래 단계를 따라주세요.

---

### 1. 데이터베이스 초기화

MySQL 서버가 실행 중인지 확인한 후, 자동 초기화 스크립트를 실행합니다:

```bash
cd server

# .env 파일 설정 (아래 참조)

# 자동 초기화 (권장) - DB 상태를 체크하고 필요한 작업만 수행
python init.py
```

**`init.py`가 자동으로:**
- ✅ DB가 있는지 체크
- ✅ 테이블이 있는지 체크
- ✅ 데이터가 있는지 체크
- ✅ 필요한 것만 생성 (있으면 건너뛰기)
- ✅ 샘플 데이터 자동 삽입 (한국공학대학교 동아리 12개)

**추가 옵션:**
```bash
python init.py --skip-sample  # 샘플 데이터 없이
python init.py --force        # 기존 데이터 삭제 후 재생성
```

**테스트 계정:**
- 관리자: `admin` / `password123`
- 학생: `student01` / `password123`

### 2. 백엔드 실행

```bash
cd server

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=club_db
JWT_SECRET_KEY=your_secret_key

# 서버 실행
python run.py
```

백엔드 서버가 `http://localhost:5000`에서 실행됩니다.

### 3. 프론트엔드 실행

```bash
cd client

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드 서버가 `http://localhost:3000`에서 실행됩니다.

## API 문서

자세한 API 문서는 [server/README.md](server/README.md)를 참조하세요.

### 주요 엔드포인트

- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/club` - 동아리 목록
- `GET /api/club/:id` - 동아리 상세
- `POST /api/apply/:club_id` - 가입 신청
- `GET /api/mypage/info` - 내 정보
- `GET /api/admin/stats` - 통계 (관리자)

## 디자인 시스템

- **기본 컬러**: 흰색, 검은색
- **포인트 컬러**: 파란색 (#2563eb)
- **스타일**: 모던하고 깔끔한 UI

## 데이터베이스 스키마

주요 테이블:
- **Student** - 학생 정보
- **Club** - 동아리 정보
- **Apply** - 가입 신청
- **Belong** - 동아리 소속
- **Post** - 게시글

자세한 스키마는 [server/schema.txt](server/schema.txt)를 참조하세요.

## 환경 변수

### 백엔드 (.env)
```
# 데이터베이스 설정
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=club_db

# JWT 설정
JWT_SECRET_KEY=your_secret_key

# 서버 설정
FLASK_ENV=development
PORT=5000
```

### 프론트엔드 (선택사항)
```
VITE_API_URL=/api
```

## 개발 가이드

### 코드 스타일
- 백엔드: Python PEP 8
- 프론트엔드: ESLint + TypeScript

### 커밋 메시지
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 코드 추가
```

## 문제 해결

### CORS 에러
- 백엔드에 Flask-CORS가 설정되어 있는지 확인
- 프론트엔드 Vite 프록시 설정 확인

### 데이터베이스 연결 실패
- MySQL 서버 실행 확인
- .env 파일의 DB 정보 확인
- 데이터베이스와 테이블 생성 확인

### JWT 토큰 만료
- 토큰 유효기간은 1시간
- 만료 시 재로그인 필요

## 라이선스

© 2025 동아리 플랫폼. All rights reserved.

