# app/api/club_api.py

from flask import Blueprint, request, jsonify, g
from app.services import club_service # 방금 만든 club_service 임포트
from app.utils.auth_decorator import login_required

# 블루프린트 생성 (/api/club 로 시작하는 URL)
club_bp = Blueprint('club', __name__, url_prefix='/api/club')

# 회원 강퇴용 블루프린트 
club_member_bp = Blueprint('club_member', __name__, url_prefix='/api/club/member')

@club_bp.route('', methods=['GET'])
def list_clubs():
    """
    동아리 전체 목록 조회 (GET /api/club)
    카테고리별 필터링 (GET /api/club?category=학술)
    (GET) 동아리 전체 목록 조회 (공개)

    Query Parameters:
        category (string, optional): 특정 카테고리의 동아리만 필터링.
        (예: GET /api/club?category=학술)

    Returns:
        200 OK: [
            {
                "Club_ID": 1,
                "Club_name": "멋쟁이코더",
                "Club_Introduction": "코딩 동아리입니다.",
                "Category": "학술",
                "Admin": "20250001"
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    
    # 쿼리 파라미터에서 'category' 값 가져오기
    category = request.args.get('category')
    
    clubs = club_service.get_all_clubs(category)
    
    if clubs is not None:
        return jsonify(clubs), 200
    else:
        return jsonify({"error": "동아리 목록을 가져오는 데 실패했습니다."}), 500

@club_bp.route('/<int:club_id>', methods=['GET'])
def get_club_detail(club_id):
    """
    동아리 상세 정보 조회 (GET /api/club/1)
    (GET) 동아리 상세 정보 조회 (공개)
    
    특정 club_id의 동아리 상세 정보와 관리자 이름을 함께 반환합니다.

    Returns:
        200 OK: {
            "Club_ID": 1,
            "Club_name": "멋쟁이코더",
            "Club_Introduction": "...",
            "Category": "학술",
            "Admin_StudentID": "20250001",
            "Admin_Name": "김제미"
        }
        404 Not Found: {"error": "해당 동아리를 찾을 수 없습니다."}
    """
    
    club = club_service.get_club_by_id(club_id)
    
    if club:
        return jsonify(club), 200
    else:
        # club_id에 해당하는 동아리가 없을 경우
        return jsonify({"error": "해당 동아리를 찾을 수 없습니다."}), 404
    

@club_bp.route('/<int:club_id>', methods=['PUT'])
@login_required # [관리자] 로그인 필수
def update_club(club_id):
    """(PUT) 동아리 정보 수정 (관리자)
    
    해당 동아리의 관리자(Admin)만 동아리 소개, 카테고리를 수정할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON): (수정할 필드만 선택적으로 전송)
    {
        "Club_Introduction": "새로운 동아리 소개입니다.",
        "Category": "스포츠"
    }

    Returns:
        200 OK: {"message": "동아리 정보가 성공적으로 수정되었습니다."}
        400 Bad Request: {"error": "수정할 데이터를 전송해주세요."}
        403 Forbidden: {"error": "동아리 정보 수정 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 동아리입니다."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "수정할 데이터를 전송해주세요."}), 400
        
    success, message = club_service.update_club_info(club_id, data, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500

@club_bp.route('/<int:club_id>/members', methods=['GET'])
@login_required # [관리자] 로그인 필수
def get_club_members_route(club_id):
    """(GET) 동아리 회원 목록 조회 (관리자)
    
    해당 동아리의 관리자(Admin)만 소속된 회원 목록을 조회할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: [
            {
                "Membership_ID": 1,
                "Student_ID": "20250002",
                "Student_Name": "이테스트",
                "Student_Email": "test2@...",
                "phone_num": "010-...",
                "Position": "일반회원"
            }, ...
        ]
        403 Forbidden: {"error": "회원 목록 조회 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 동아리입니다."}
    """
    request_student_id = g.user['Student_ID']
    
    members, message = club_service.get_club_members(club_id, request_student_id)
    
    if members is not None:
        return jsonify(members), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500

# --- [회원 강퇴 API (새 블루프린트)] ---

@club_member_bp.route('/<int:membership_id>', methods=['DELETE'])
@login_required # [관리자] 로그인 필수
def remove_member(membership_id):
    """(DELETE) 동아리 회원 강퇴 (관리자)
    
    해당 동아리의 관리자(Admin)만 회원을 강퇴(Belong 테이블에서 삭제)시킬 수 있습니다.
    관리자 본인은 강퇴할 수 없습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: {"message": "회원이 성공적으로 삭제되었습니다."}
        403 Forbidden: {"error": "회원 삭제 권한이 없습니다."}
                     {"error": "동아리 관리자(본인)는 강퇴할 수 없습니다."}
        404 Not Found: {"error": "존재하지 않는 회원 ID입니다."}
    """
    request_student_id = g.user['Student_ID']
    
    success, message = club_service.remove_club_member(membership_id, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500