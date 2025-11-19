@echo off
REM 동아리 플랫폼 백엔드 & 프론트엔드 동시 실행 스크립트
REM Windows용

setlocal EnableDelayedExpansion

REM 프로세스 ID 저장 변수
set "BACKEND_PID="
set "FRONTEND_PID="

REM Ctrl+C 핸들러 등록
if "%1"=="cleanup" goto :cleanup

echo ======================================================================
echo 동아리 플랫폼 서버를 시작합니다...
echo ======================================================================

REM 1. 백엔드 환경 확인
echo.
echo [1/2] 백엔드 환경 확인...

if not exist "server\.env" (
    echo [오류] server\.env 파일이 없습니다.
    echo setup.bat를 먼저 실행하거나 .env 파일을 생성해주세요.
    pause
    exit /b 1
)

if not exist "server\venv" (
    echo [오류] Python 가상환경이 없습니다.
    echo setup.bat를 먼저 실행해주세요.
    pause
    exit /b 1
)

REM 2. 프론트엔드 환경 확인
echo.
echo [2/2] 프론트엔드 환경 확인...

if not exist "client\node_modules" (
    echo [경고] node_modules가 없습니다. 설치를 시작합니다...
    cd client
    call npm install
    cd ..
)

REM 3. 백엔드 서버 시작
echo.
echo 백엔드 서버 시작 중...
cd server
start /B cmd /c "venv\Scripts\activate.bat && python run.py" > ..\backend.log 2>&1
cd ..

REM 백엔드 시작 대기 (3초)
timeout /t 3 /nobreak > nul

echo [완료] 백엔드 서버가 시작되었습니다.

REM 4. 프론트엔드 빌드 및 서버 시작
echo.
echo 프론트엔드 빌드 중...
cd client
call npm run build
if %errorlevel% neq 0 (
    echo [오류] 프론트엔드 빌드 실패.
    cd ..
    taskkill /F /FI "WINDOWTITLE eq Administrator:  python run.py" > nul 2>&1
    pause
    exit /b 1
)
echo [완료] 프론트엔드 빌드 완료.

echo.
echo 프론트엔드 서버 시작 중...
start /B cmd /c "npm run preview" > ..\frontend.log 2>&1
cd ..

REM 프론트엔드 시작 대기 (3초)
timeout /t 3 /nobreak > nul

echo [완료] 프론트엔드 서버가 시작되었습니다.

REM 완료 메시지
echo.
echo ======================================================================
echo 모든 서버가 실행되었습니다!
echo ======================================================================
echo.
echo 백엔드:     http://127.0.0.1:5000
echo 프론트엔드: http://localhost:4173 (Vite Preview 기본 포트)
echo.
echo 종료하려면 Ctrl+C를 누르거나 이 창을 닫으세요.
echo 또는 아무 키나 눌러 서버를 종료할 수 있습니다.
echo.

REM 사용자 입력 대기 (종료 트리거)
pause > nul

:cleanup
echo.
echo 종료 중...

REM Python 프로세스 종료
echo 백엔드 프로세스 종료 중...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq python*" > nul 2>&1
wmic process where "commandline like '%%run.py%%'" delete > nul 2>&1

REM Node 프로세스 종료
echo 프론트엔드 프로세스 종료 중...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq node*" > nul 2>&1
wmic process where "commandline like '%%vite%%preview%%'" delete > nul 2>&1

REM 로그 파일 정리
if exist backend.log del backend.log
if exist frontend.log del frontend.log

echo 모든 프로세스가 종료되었습니다.
timeout /t 2 /nobreak > nul
exit /b 0

