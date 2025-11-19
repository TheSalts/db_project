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
