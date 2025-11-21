# app/api/auth_api.py
import jwt
import datetime
import bcrypt
from flask import Blueprint, request, jsonify, current_app
from app.services import auth_service

# 블루프린트 생성 (/api/auth 로 시작하는 URL)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입 API"""
    """(POST) 신규 학생 회원가입

    클라이언트로부터 학생 정보를 JSON으로 받아 DB에 저장합니다.
    비밀번호는 자동으로 해시(hash) 처리됩니다.

    Body (JSON):
    {
        "Student_ID": "string",
        "Login_ID": "string",
        "Pw": "string",
        "Name": "string",
        "phone_num": "string (optional)",
        "Email": "string (optional)"
    }
    
    Returns:
        201 Created: {"message": "회원가입 성공"}
        400 Bad Request: {"error": "필수 값이 누락되었습니다."}
        409 Conflict: {"error": "이미 사용 중인 아이디입니다."}
                     {"error": "이미 등록된 학번입니다."}
    """
    data = request.get_json()
    
    # 필수 값 체크
    if not all([data.get('Student_ID'), data.get('Login_ID'), data.get('Pw'), data.get('Name')]):
        return jsonify({"error": "필수 값(학번, 아이디, 비밀번호, 이름)이 누락되었습니다."}), 400

    success, message = auth_service.create_user(data)
    
    if success:
        return jsonify({"message": message}), 201 # 201 Created
    else:
        # 아이디 중복 같은 에러
        return jsonify({"error": message}), 409 # 409 Conflict (중복) 또는 500

@auth_bp.route('/login', methods=['POST'])
def login():
    print(">>> 로그인 요청 수신됨") # 디버깅용 로그
    """로그인 API"""
    """(POST) 학생 로그인

    Login_ID와 Pw를 받아 검증 후, 성공 시 JWT 인증 토큰을 발급합니다.
    
    Body (JSON):
    {
        "Login_ID": "string",
        "Pw": "string"
    }

    Returns:
        200 OK: {"message": "로그인 성공!", "token": "JWT_TOKEN_HERE"}
        400 Bad Request: {"error": "아이디와 비밀번호를 모두 입력해주세요."}
        401 Unauthorized: {"error": "존재하지 않는 아이디입니다."}
                         {"error": "비밀번호가 일치하지 않습니다."}
    """
    data = request.get_json()
    login_id = data.get('Login_ID')
    password = data.get('Pw')

    if not login_id or not password:
        return jsonify({"error": "아이디와 비밀번호를 모두 입력해주세요."}), 400

    # 1. 서비스에 유저 정보 요청
    user = auth_service.get_user_by_login_id(login_id)

    if user is None:
        return jsonify({"error": "존재하지 않는 아이디입니다."}), 401 # 401 Unauthorized

    # 2. 비밀번호 검증 (DB의 해시된 비번 vs 지금 입력한 비번)
    password_encoded = password.encode('utf-8')
    hashed_password_from_db = user['Pw'].encode('utf-8') # DB에서 가져온 해시
    
    if bcrypt.checkpw(password_encoded, hashed_password_from_db):
        # 3. 로그인 성공: JWT 토큰 생성
        expiration_hours = current_app.config.get('JWT_EXPIRATION_HOURS', 24)
        payload = {
            'Student_ID': user['Student_ID'],
            'iat': datetime.datetime.now(datetime.timezone.utc),  # 발급 시간
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expiration_hours)
        }
        secret = current_app.config['JWT_SECRET_KEY']
        algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
        token = jwt.encode(payload, secret, algorithm=algorithm)
        
        return jsonify({
            "message": "로그인 성공!", 
            "token": token,
            "expires_in": expiration_hours * 3600  # 초 단위로 만료 시간 반환
        }), 200
    else:
        # 비밀번호 불일치
        return jsonify({"error": "비밀번호가 일치하지 않습니다."}), 401