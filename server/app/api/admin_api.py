# app/api/admin_api.py

from flask import Blueprint, jsonify, g
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