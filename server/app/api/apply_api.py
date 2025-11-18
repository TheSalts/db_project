# app/api/apply_api.py

from flask import Blueprint, request, jsonify, g
from app.services import apply_service
from app.utils.auth_decorator import login_required # '문지기' 임포트

# 블루프린트 생성 (/api/apply 로 시작)
apply_bp = Blueprint('apply', __name__, url_prefix='/api/apply')

@apply_bp.route('/<int:club_id>', methods=['POST'])
@login_required # [학생] 가입 신청 (로그인 필수)
def submit_application(club_id):
    """(POST) 동아리 가입 신청 (학생)
    
    로그인한 학생이 특정 club_id의 동아리에 가입 신청서를 제출합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON):
    {
        "Self_Introduction": "string (optional, 자기소개)"
    }

    Returns:
        201 Created: {"message": "가입 신청이 완료되었습니다."}
        409 Conflict: {"error": "이미 해당 동아리에 가입 신청했거나 가입된 상태입니다."}
        500 Internal Server Error: {"error": "..."}
    """
    student_id = g.user['Student_ID']
    data = request.get_json()
    
    success, message = apply_service.create_application(student_id, club_id, data)
    
    if success:
        return jsonify({"message": message}), 201 # 201 Created
    else:
        # (예: 중복 신청)
        return jsonify({"error": message}), 409 # 409 Conflict

@apply_bp.route('/manage/<int:club_id>', methods=['GET'])
@login_required # [관리자] 신청 목록 조회 (로그인 필수)
def get_club_applications(club_id):
    """(GET) 동아리 신청 목록 조회 (관리자)
    
    해당 동아리의 관리자(Admin)가 '대기' 상태인 가입 신청 목록을 조회합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: [
            {
                "Application_ID": 1,
                "Student_ID": "20250003",
                "Student_Name": "박신청",
                "Student_Email": "apply@...",
                "Self_Introduction": "열심히 하겠습니다.",
                "Application_Date": "2025-11-18T11:00:00",
                "Status": "대기"
            }, ...
        ]
        403 Forbidden: {"error": "조회 권한이 없습니다 (관리자 아님)."}
        404 Not Found: {"error": "존재하지 않는 동아리입니다."}
    """
    request_student_id = g.user['Student_ID'] # 요청자(관리자)의 학번
    
    applications, message = apply_service.get_applications_for_club(club_id, request_student_id)
    
    if applications is not None:
        return jsonify(applications), 200
    else:
        # (예: 권한 없음, 존재하지 않는 동아리)
        if "권한" in message:
            return jsonify({"error": message}), 403 # 403 Forbidden (권한 없음)
        if "존재" in message:
            return jsonify({"error": message}), 404 # 404 Not Found
        return jsonify({"error": message}), 500 # 서버 에러

@apply_bp.route('/manage/<int:application_id>', methods=['PUT'])
@login_required # [관리자] 신청 상태 변경 (로그인 필수)
def update_application(application_id):
    """(PUT) 신청서 상태 변경 (승인/거절) (관리자)
    
    관리자가 특정 application_id의 상태를 '승인' 또는 '거절'로 변경합니다.
    '승인' 시 DB 트리거가 자동으로 'Belong' 테이블에 회원을 추가합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON):
    {
        "Status": "승인"  (또는 "거절")
    }

    Returns:
        200 OK: {"message": "신청서가 '승인' 처리되었습니다."}
        400 Bad Request: {"error": "Status는 '승인' 또는 '거절'이어야 합니다."}
        403 Forbidden: {"error": "처리 권한이 없습니다 (관리자 아님)."}
        404 Not Found: {"error": "존재하지 않는 신청서입니다."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    status = data.get('Status') # '승인' 또는 '거절'

    if status not in ['승인', '거절']:
        return jsonify({"error": "Status는 '승인' 또는 '거절'이어야 합니다."}), 400

    success, message = apply_service.update_application_status(application_id, status, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        # (예: 권한 없음, 존재하지 않는 신청서)
        if "권한" in message:
            return jsonify({"error": message}), 403 # 403 Forbidden
        if "존재" in message:
            return jsonify({"error": message}), 404 # 404 Not Found
        return jsonify({"error": message}), 500