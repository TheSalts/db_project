#!/bin/bash

# 동아리 플랫폼 백엔드 & 프론트엔드 동시 실행 스크립트
# macOS/Linux용

set -e  # 오류 발생 시 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로세스 ID 저장 변수
BACKEND_PID=""
FRONTEND_PID=""

# 종료 함수 (Ctrl+C 시 두 프로세스 모두 종료)
cleanup() {
    echo "\n${YELLOW}종료 중...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo "${BLUE}백엔드 프로세스 종료 중...${NC}"
        kill -TERM $BACKEND_PID 2>/dev/null || true
        wait $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "${BLUE}프론트엔드 프로세스 종료 중...${NC}"
        kill -TERM $FRONTEND_PID 2>/dev/null || true
        wait $FRONTEND_PID 2>/dev/null || true
    fi
    
    # 남아있는 자식 프로세스 모두 종료
    pkill -P $$ 2>/dev/null || true
    
    echo "${GREEN}모든 프로세스가 종료되었습니다.${NC}"
    exit 0
}

# 시그널 핸들러 등록
trap cleanup SIGINT SIGTERM

echo "======================================================================"
echo "${GREEN} 동아리 플랫폼 서버를 시작합니다...${NC}"
echo "======================================================================"

# 1. 백엔드 환경 확인
echo "\n${BLUE}[1/2]${NC} 백엔드 환경 확인..."

if [ ! -f "server/.env" ]; then
    echo "${RED}✗${NC} server/.env 파일이 없습니다."
    echo "setup.sh를 먼저 실행하거나 .env 파일을 생성해주세요."
    exit 1
fi

if [ ! -d "server/venv" ]; then
    echo "${RED}✗${NC} Python 가상환경이 없습니다."
    echo "setup.sh를 먼저 실행해주세요."
    exit 1
fi

# 2. 프론트엔드 환경 확인
echo "\n${BLUE}[2/2]${NC} 프론트엔드 환경 확인..."

if [ ! -d "client/node_modules" ]; then
    echo "${YELLOW}⚠️  node_modules가 없습니다. 설치를 시작합니다...${NC}"
    cd client
    npm install
    cd ..
fi

# 3. 백엔드 서버 시작
echo "\n${GREEN}백엔드 서버 시작 중...${NC}"
cd server
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# 백엔드 시작 대기 (2초)
sleep 2

# 백엔드 프로세스 확인
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "${RED}✗${NC} 백엔드 서버 시작 실패."
    exit 1
fi

echo "${GREEN}✓${NC} 백엔드 서버가 시작되었습니다. (PID: $BACKEND_PID)"

# 4. 프론트엔드 빌드 및 서버 시작
echo "\n${GREEN}프론트엔드 빌드 중...${NC}"
cd client
npm run build
if [ $? -ne 0 ]; then
    echo "${RED}✗${NC} 프론트엔드 빌드 실패."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi
echo "${GREEN}✓${NC} 프론트엔드 빌드 완료."

echo "\n${GREEN}프론트엔드 서버 시작 중...${NC}"
npm run preview &
FRONTEND_PID=$!
cd ..

# 프론트엔드 시작 대기 (2초)
sleep 2

# 프론트엔드 프로세스 확인
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "${RED}✗${NC} 프론트엔드 서버 시작 실패."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "${GREEN}✓${NC} 프론트엔드 서버가 시작되었습니다. (PID: $FRONTEND_PID)"

# 완료 메시지
echo ""
echo "======================================================================"
echo "${GREEN}✅ 모든 서버가 실행되었습니다!${NC}"
echo "======================================================================"
echo ""
echo "${BLUE}백엔드:${NC}  http://127.0.0.1:5000"
echo "${BLUE}프론트엔드:${NC} http://localhost:4173 (Vite Preview 기본 포트)"
echo ""
echo "${YELLOW}종료하려면 Ctrl+C를 누르세요.${NC}"
echo ""

# 프로세스가 종료될 때까지 대기
while true; do
    # 백엔드와 프론트엔드 프로세스가 모두 살아있는지 확인
    if ! kill -0 $BACKEND_PID 2>/dev/null || ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "\n${RED}프로세스 중 하나가 예상치 못하게 종료되었습니다.${NC}"
        cleanup
    fi
    sleep 1
done
