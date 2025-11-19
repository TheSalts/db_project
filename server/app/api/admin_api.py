# app/api/admin_api.py

from flask import Blueprint, jsonify, request, g
from app.services import admin_service
from app.utils.auth_decorator import login_required

# 블루프린트 생성 (/api/admin 로 시작)
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
@login_required # [관리자] 1차: 로그인 필수
def get_statistics():
    """(GET) 사이트 전체 통계 조회 (사이트 관리자)
    
    [관리자 전용]
    로그인한 학생의 'Role'이 '관리자'일 경우에만 사이트 전체 통계를 반환합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: {
            "total_students": 150,
            "total_clubs": 30,
            "pending_applications": 5,
            "clubs_by_category": [
                {"Category": "학술", "count": 10},
                {"Category": "스포츠", "count": 8}
            ]
        }
        403 Forbidden: {"error": "통계 조회 권한이 없습니다 (사이트 관리자 아님)."}
        500 Internal Server Error: {"error": "..."}
    """
    
    # 2차: Role 검사는 서비스 레이어(admin_service)에서 수행
    request_student_id = g.user['Student_ID'] 
    
    statistics, message = admin_service.get_site_statistics(request_student_id)
    
    if statistics is not None:
        return jsonify(statistics), 200
    else:
        # (예: 권한 없음)
        if "권한" in message:
            return jsonify({"error": message}), 403 # 403 Forbidden
        return jsonify({"error": message}), 500 # 서버 에러

@admin_bp.route('/clubs', methods=['POST'])
@login_required
def create_new_club():
    """
    (POST) 새 동아리 생성 (사이트 관리자 전용)
    
    [사이트 관리자 전용]
    로그인한 학생의 'Role'이 '관리자'일 경우에만 새 동아리를 생성할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>
    
    Body (JSON):
    {
        "Club_name": "string (required)",
        "Club_Introduction": "string (optional)",
        "Category": "string (optional, default: '기타')",
        "Admin": "string (required, 관리자 학번)"
    }
    
    Returns:
        201 Created: {"message": "동아리가 성공적으로 생성되었습니다.", "Club_ID": 1}
        400 Bad Request: {"error": "필수 필드가 누락되었습니다."}
        403 Forbidden: {"error": "동아리 생성 권한이 없습니다 (사이트 관리자 아님)."}
        404 Not Found: {"error": "존재하지 않는 학번입니다."}
        500 Internal Server Error: {"error": "..."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    
    success, result = admin_service.create_club(data, request_student_id)
    
    if success:
        # result는 club_id (int)
        return jsonify({"message": "동아리가 성공적으로 생성되었습니다.", "Club_ID": result}), 201
    else:
        # result는 에러 메시지 (str)
        if "권한" in result:
            return jsonify({"error": result}), 403
        if "존재하지 않는" in result:
            return jsonify({"error": result}), 404
        if "필수" in result:
            return jsonify({"error": result}), 400
        return jsonify({"error": result}), 500