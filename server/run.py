# run.py
import os
from app import create_app

app = create_app()

# .env 파일에서 설정 값 가져오기
env = os.environ.get('FLASK_ENV', 'development')
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    print("=====================================================")
    print(f"🚀 [INFO] 동아리 플랫폼 백엔드 서버를 시작합니다...")
    print(f"🌍 [INFO] 실행 환경 (FLASK_ENV): {env}")
    print(f"🔗 [INFO] 서버 주소: http://127.0.0.1:{port}")
    print("=====================================================")
    
    app.run(host='0.0.0.0', port=port, debug=(env == 'development'))
