#!/bin/bash

# 동아리 플랫폼 자동 설정 스크립트
# macOS/Linux용

set -e  # 오류 발생 시 중단

echo "======================================================================"
echo "🚀 동아리 플랫폼 자동 설정을 시작합니다..."
echo "======================================================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. .env 파일 확인
echo -e "\n${BLUE}[1/5]${NC} 환경 변수 설정 확인..."
if [ ! -f "server/.env" ]; then
    echo -e "${YELLOW}⚠️  .env 파일이 없습니다.${NC}"
    echo "server/.env 파일을 생성해주세요."
    echo ""
    echo "예시:"
    echo "DB_HOST=localhost"
    echo "DB_USER=root"
    echo "DB_PASSWORD=your_password"
    echo "DB_NAME=club_db"
    echo "JWT_SECRET_KEY=your_secret_key"
    echo "FLASK_ENV=development"
    echo "PORT=5000"
    exit 1
else
    echo -e "${GREEN}✓${NC} .env 파일이 있습니다."
fi

# 2. Python 가상환경 확인 및 생성
echo -e "\n${BLUE}[2/5]${NC} Python 가상환경 설정..."
cd server
if [ ! -d "venv" ]; then
    echo "가상환경을 생성합니다..."
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓${NC} 가상환경이 활성화되었습니다."

# 3. Python 의존성 설치
echo -e "\n${BLUE}[3/5]${NC} Python 패키지 설치..."
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Python 패키지 설치 완료."

# 4. 데이터베이스 초기화
echo -e "\n${BLUE}[4/5]${NC} 데이터베이스 초기화..."
python init.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 데이터베이스 초기화 완료."
else
    echo -e "${RED}✗${NC} 데이터베이스 초기화 실패."
    echo "MySQL이 실행 중인지, .env 설정이 올바른지 확인하세요."
    exit 1
fi

cd ..

# 5. 프론트엔드 의존성 설치
echo -e "\n${BLUE}[5/5]${NC} 프론트엔드 패키지 설치..."
cd client
if [ ! -d "node_modules" ]; then
    npm install
    echo -e "${GREEN}✓${NC} 프론트엔드 패키지 설치 완료."
else
    echo -e "${GREEN}✓${NC} 프론트엔드 패키지가 이미 설치되어 있습니다."
fi
cd ..

# 완료
echo ""
echo "======================================================================"
echo -e "${GREEN}✅ 설정이 완료되었습니다!${NC}"
echo "======================================================================"
echo ""
echo "이제 서버를 실행할 수 있습니다:"
echo ""
echo "1. 백엔드 실행:"
echo "   cd server"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "2. 프론트엔드 실행 (새 터미널):"
echo "   cd client"
echo "   npm run dev"
echo ""
echo "3. 브라우저에서 http://localhost:3000 접속"
echo ""
echo "💡 테스트 계정: admin / password123"
echo ""

