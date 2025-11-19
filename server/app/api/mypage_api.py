# app/api/mypage_api.py

from flask import Blueprint, request, jsonify, g
from app.services import mypage_service
from app.utils.auth_decorator import login_required # 만든 '문지기' 임포트!

# 블루프린트 생성 (/api/mypage 로 시작)
mypage_bp = Blueprint('mypage', __name__, url_prefix='/api/mypage')

@mypage_bp.route('/info', methods=['GET'])
@login_required #이 API는 로그인이 필요함
def get_my_info():
    """(GET) 내 정보 조회 (로그인 필수)
    
    로그인한 학생 본인의 정보를 조회합니다. (비밀번호 제외)
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: {
            "Student_ID": "20250001",
            "Login_ID": "testuser",
            "Name": "김테스트",
            "phone_num": "010-...",
            "Email": "test@...",
            "Role": "일반"
        }
        404 Not Found: {"error": "사용자 정보를 찾을 수 없습니다."}
    """
    student_id = g.user['Student_ID'] 
    
    user_info = mypage_service.get_user_info(student_id)
    
    if user_info:
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "사용자 정보를 찾을 수 없습니다."}), 404

@mypage_bp.route('/info', methods=['PUT'])
@login_required 
def update_my_info():
    """(PUT) 내 정보 수정 (로그인 필수)
    
    로그인한 학생 본인의 정보를 수정합니다.
    (Name, phone_num, Email, Pw 중 변경할 필드만 선택적으로 전송)
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON): (수정할 필드만 전송)
    {
        "Name": "김제미",
        "phone_num": "010-1234-5678",
        "Pw": "new_password123" 
    }

    Returns:
        200 OK: {"message": "정보가 성공적으로 수정되었습니다."}
        400 Bad Request: {"error": "변경할 데이터를 전송해주세요."}
        409 Conflict: {"error": "이미 사용 중인 이메일입니다."}
    """
    student_id = g.user['Student_ID']
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "변경할 데이터를 전송해주세요."}), 400

    success, message = mypage_service.update_user_info(student_id, data)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        # (예: 이메일 중복)
        return jsonify({"error": message}), 409 # 409 Conflict

@mypage_bp.route('/applications', methods=['GET'])
@login_required
def get_my_applications_route():
    """(GET) 내 가입 신청 현황 조회 (로그인 필수)
    
    로그인한 학생이 신청한 모든 동아리의 신청 현황을 조회합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: [
            {
                "Application_ID": 1,
                "Club_ID": 1,
                "Club_name": "멋쟁이코더",
                "Self_Introduction": "열심히 하겠습니다.",
                "Application_Date": "2025-11-18T11:00:00",
                "Status": "대기" (또는 "승인", "거절")
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    student_id = g.user['Student_ID']
    applications = mypage_service.get_my_applications(student_id)
    
    if applications is not None:
        return jsonify(applications), 200
    else:
        return jsonify({"error": "신청 현황을 가져오는 데 실패했습니다."}), 500

@mypage_bp.route('/clubs', methods=['GET'])
@login_required
def get_my_clubs_route():
    """(GET) 내가 가입한 동아리 목록 조회 (로그인 필수)
    
    로그인한 학생이 'Belong' (소속)된 모든 동아리 목록을 조회합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: [
            {
                "Membership_ID": 1,
                "Club_ID": 1,
                "Club_name": "멋쟁이코더",
                "Category": "학술",
                "Position": "일반회원" (또는 "회장")
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    student_id = g.user['Student_ID']
    clubs = mypage_service.get_my_clubs(student_id)
    
    if clubs is not None:
        return jsonify(clubs), 200
    else:
        return jsonify({"error": "동아리 목록을 가져오는 데 실패했습니다."}), 500
    
@mypage_bp.route('/comments', methods=['GET'])
@login_required
def get_my_comments_route():
    """(GET) 내가 작성한 댓글 목록 조회 (로그인 필수)
    
    로그인한 학생이 작성한 모든 댓글을 조회합니다.
    댓글이 달린 원본 동아리 이름(Club_name)도 함께 반환됩니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: [
            {
                "Comment_ID": 1,
                "Content": "좋은 공지네요!",
                "created_at": "2025-11-19T10:01:00",
                "Post_ID": 1,
                "Club_ID": 1,
                "Club_name": "멋쟁이코더"
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    student_id = g.user['Student_ID']
    comments = mypage_service.get_my_comments(student_id)
    
    if comments is not None:
        return jsonify(comments), 200
    else:
        return jsonify({"error": "댓글 목록을 가져오는 데 실패했습니다."}), 500