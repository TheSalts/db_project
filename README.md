# 동아리 플랫폼

버그 / 미구현 / 잘못 구현한 내용 있는지 확인해주세요

---

## 설치 방법

- Python 및 nodejs(npm)이 설치되어 있어야 합니다.

`server/.env` 파일 작성

```env
# .env

# Flask
FLASK_ENV=development
PORT=8000

# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root  # MySQL 비밀번호
DB_NAME=club_db

# JWT
JWT_SECRET_KEY=our-project-super-secret-key-123
```

### macOS & Linux

`setup.sh` 실행 후 `start.sh` 실행

### Windows

`setup.bat` 실행 후 `start.bat` 실행

- `.bat` 파일은 테스트되지 않음

## 샘플 데이터 계정 정보

모든 계정의 비밀번호는 `password123`입니다.

| 역할 | Login ID | 비밀번호 | 설명 |
|------|----------|----------|------|
| 관리자 | `admin` | `password123` | 사이트 관리자 |
| 일반 학생 | `student01` | `password123` | 일반 학생 계정 1 |
| 일반 학생 | `student02` | `password123` | 일반 학생 계정 2 |
| 일반 학생 | `student03` | `password123` | 일반 학생 계정 3 |
| 일반 학생 | `student04` | `password123` | 일반 학생 계정 4 |
| 일반 학생 | `student05` | `password123` | 일반 학생 계정 5 |

### 동아리 관리자 계정

#### 사회분과

| Login ID | 비밀번호 | 동아리 |
|----------|----------|--------|
| `nanum_admin` | `password123` | 나눔 |
| `rotaract_admin` | `password123` | 로타랙트 |
| `masil_admin` | `password123` | 마실 |
| `ccc_admin` | `password123` | CCC |
| `ouiparfum_admin` | `password123` | Oui Parfum |
| `thetiki_admin` | `password123` | The Tiki |

#### 학술분과

| Login ID | 비밀번호 | 동아리 |
|----------|----------|--------|
| `seabueong_admin` | `password123` | 씨부엉 |
| `aram_admin` | `password123` | 아람 |
| `teamnc_admin` | `password123` | 팀엔써 |
| `hyeium_admin` | `password123` | 혜윰 |
| `cir_admin` | `password123` | CIR |
| `ham_admin` | `password123` | HAM |

#### 체육분과

| Login ID | 비밀번호 | 동아리 |
|----------|----------|--------|
| `dungkids_admin` | `password123` | 덩키즈 |
| `sansaram_admin` | `password123` | 산사람 |
| `santakgu_admin` | `password123` | 산탁구 |
| `seoseong_admin` | `password123` | 서성 |
| `winners_admin` | `password123` | 위너스 |
| `teamfight_admin` | `password123` | 팀파이트 |
| `insane_admin` | `password123` | INSANE |
| `wing_admin` | `password123` | WING |
