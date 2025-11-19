@echo off
REM 동아리 플랫폼 자동 설정 스크립트
REM Windows용

echo ======================================================================
echo 동아리 플랫폼 자동 설정을 시작합니다...
echo ======================================================================

REM 1. .env 파일 확인
echo.
echo [1/5] 환경 변수 설정 확인...
if not exist "server\.env" (
    echo [경고] .env 파일이 없습니다.
    echo server\.env 파일을 생성해주세요.
    echo.
    echo 예시:
    echo DB_HOST=localhost
    echo DB_USER=root
    echo DB_PASSWORD=your_password
    echo DB_NAME=club_db
    echo JWT_SECRET_KEY=your_secret_key
    echo FLASK_ENV=development
    echo PORT=5000
    pause
    exit /b 1
) else (
    echo [완료] .env 파일이 있습니다.
)

REM 2. Python 가상환경 확인 및 생성
echo.
echo [2/5] Python 가상환경 설정...
cd server
if not exist "venv" (
    echo 가상환경을 생성합니다...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo [완료] 가상환경이 활성화되었습니다.

REM 3. Python 의존성 설치
echo.
echo [3/5] Python 패키지 설치...
pip install -q -r requirements.txt
if %errorlevel% equ 0 (
    echo [완료] Python 패키지 설치 완료.
) else (
    echo [오류] Python 패키지 설치 실패.
    cd ..
    pause
    exit /b 1
)

REM 4. 데이터베이스 초기화
echo.
echo [4/5] 데이터베이스 초기화...
python init.py
if %errorlevel% equ 0 (
    echo [완료] 데이터베이스 초기화 완료.
) else (
    echo [오류] 데이터베이스 초기화 실패.
    echo MySQL이 실행 중인지, .env 설정이 올바른지 확인하세요.
    cd ..
    pause
    exit /b 1
)

cd ..

REM 5. 프론트엔드 의존성 설치
echo.
echo [5/5] 프론트엔드 패키지 설치...
cd client
if not exist "node_modules" (
    call npm install
    echo [완료] 프론트엔드 패키지 설치 완료.
) else (
    echo [완료] 프론트엔드 패키지가 이미 설치되어 있습니다.
)
cd ..

REM 완료
echo.
echo ======================================================================
echo 설정이 완료되었습니다!
echo ======================================================================
echo.
echo 이제 서버를 실행할 수 있습니다:
echo.
echo 1. 백엔드 실행:
echo    cd server
echo    venv\Scripts\activate.bat
echo    python run.py
echo.
echo 2. 프론트엔드 실행 (새 터미널):
echo    cd client
echo    npm run dev
echo.
echo 3. 브라우저에서 http://localhost:3000 접속
echo.
echo 테스트 계정: admin / password123
echo.
pause

