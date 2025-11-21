# app/utils/auth_decorator.py

import jwt
from functools import wraps
from flask import request, jsonify, current_app, g

def login_required(f):
    """
    로그인 여부를 확인하는 데코레이터.
    - 유효한 토큰이면: g.user에 'Student_ID' 저장
    - 유효하지 않으면: 401 에러 반환
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # 1. HTTP 헤더에서 토큰 가져오기
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # "Bearer <token>" 형식인지 확인
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            return jsonify({"error": "로그인 토큰이 필요합니다."}), 401

        # 2. 토큰 디코딩 (유효성 검사)
        try:
            secret = current_app.config['JWT_SECRET_KEY']
            algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
            payload = jwt.decode(token, secret, algorithms=[algorithm])
            
            # g (Flask의 context)에 유저 정보 저장
            # 이제 이 요청을 처리하는 동안 g.user로 Student_ID를 꺼낼 수 있음
            g.user = {
                'Student_ID': payload['Student_ID']
            }
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "토큰이 만료되었습니다. 다시 로그인해주세요."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "유효하지 않은 토큰입니다."}), 401
        
        # 3. 토큰이 유효하면 원래 함수 실행
        return f(*args, **kwargs)

    return decorated_function