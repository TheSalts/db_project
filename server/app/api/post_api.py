# app/api/post_api.py

from flask import Blueprint, request, jsonify, g
from app.services import post_service
from app.utils.auth_decorator import login_required

# 블루프린트 2개 생성 (주소가 다르므로)
post_club_bp = Blueprint('post_club', __name__, url_prefix='/api/club')
post_manage_bp = Blueprint('post_manage', __name__, url_prefix='/api/post')

# --- 1. /api/club/<id>/post ---

@post_club_bp.route('/<int:club_id>/post', methods=['GET'])
def get_posts(club_id):
    """(GET) 특정 동아리 게시글 목록 조회 (공개)
    
    해당 club_id의 모든 게시글을 작성일 내림차순으로 조회합니다.
    관리자 이름(Admin_Name)도 함께 반환됩니다.

    Returns:
        200 OK: [
            {
                "Post_ID": 1,
                "Club_ID": 1,
                "Content": "첫 번째 공지입니다.",
                "post_date": "2025-11-18T10:00:00",
                "Admin_Name": "김제미"
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    posts = post_service.get_posts_by_club_id(club_id)
    
    if posts is not None:
        return jsonify(posts), 200
    else:
        return jsonify({"error": "게시글 목록 조회에 실패했습니다."}), 500

@post_club_bp.route('/<int:club_id>/post', methods=['POST'])
@login_required # [관리자] 로그인 필수
def create_new_post(club_id):
    """(POST) 특정 동아리 게시글 작성 (관리자)
    
    해당 동아리의 관리자(Admin)만 새 게시글을 작성할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON):
    {
        "Content": "새로운 공지사항 내용입니다."
    }

    Returns:
        201 Created: {"message": "게시글이 성공적으로 작성되었습니다.", "Post_ID": 2}
        400 Bad Request: {"error": "'Content'가 필요합니다."}
        403 Forbidden: {"error": "게시글 작성 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 동아리입니다."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    
    if not data or 'Content' not in data:
        return jsonify({"error": "Content'가 필요합니다."}), 400
        
    success, result = post_service.create_post(club_id, data, request_student_id)
    
    if success:
        # result는 {"message": "...", "Post_ID": 1} 딕셔너리
        return jsonify(result), 201
    else:
        # result는 "에러 메시지" 문자열
        if "권한" in result:
            return jsonify({"error": result}), 403
        if "존재" in result:
            return jsonify({"error": result}), 404
        return jsonify({"error": result}), 500

# --- 2. /api/post/<id> ---

@post_manage_bp.route('/<int:post_id>', methods=['PUT'])
@login_required # [관리자] 로그인 필수
def update_existing_post(post_id):
    """(PUT) 게시글 수정 (관리자)
    
    해당 게시글을 작성한 동아리의 관리자(Admin)만 수정할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON):
    {
        "Content": "수정된 공지사항 내용입니다."
    }

    Returns:
        200 OK: {"message": "게시글이 성공적으로 수정되었습니다."}
        400 Bad Request: {"error": "'Content'가 필요합니다."}
        403 Forbidden: {"error": "게시글 수정 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 게시글입니다."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    
    if not data or 'Content' not in data:
        return jsonify({"error": "Content'가 필요합니다."}), 400
        
    success, message = post_service.update_post(post_id, data, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500

@post_manage_bp.route('/<int:post_id>', methods=['DELETE'])
@login_required # [관리자] 로그인 필수
def delete_existing_post(post_id):
    """(DELETE) 게시글 삭제 (관리자)
    
    해당 게시글을 작성한 동아리의 관리자(Admin)만 삭제할 수 있습니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: {"message": "게시글이 성공적으로 삭제되었습니다."}
        403 Forbidden: {"error": "게시글 삭제 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 게시글입니다."}
    """
    request_student_id = g.user['Student_ID']
    
    success, message = post_service.delete_post(post_id, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500
    

    # 1. /api/club/<int:club_id>/post (특정 동아리에 대한 목록/작성)
    # 2. /api/post/<int:post_id> (특정 게시글 수정/삭제)