# app/api/comment_api.py

from flask import Blueprint, request, jsonify, g
from app.services import comment_service
from app.utils.auth_decorator import login_required

# 블루프린트 생성 (주소 체계가 2개라 2개 만듦)
comment_post_bp = Blueprint('comment_post', __name__, url_prefix='/api/post')
comment_manage_bp = Blueprint('comment_manage', __name__, url_prefix='/api/comment')


# --- /api/post/<id>/... ---

@comment_post_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """(GET) 특정 게시글 댓글 목록 조회 (공개)
    
    해당 post_id의 모든 댓글을 작성순(ASC)으로 조회합니다.
    댓글 작성자 이름도 함께 반환됩니다.

    Returns:
        200 OK: [
            {
                "Comment_ID": 1,
                "Post_ID": 1,
                "Student_ID": "20250002",
                "Student_Name": "이테스트",
                "Content": "좋은 공지네요!",
                "created_at": "2025-11-19T10:01:00"
            }, ...
        ]
        500 Internal Server Error: {"error": "..."}
    """
    comments = comment_service.get_comments_for_post(post_id)
    
    if comments is not None:
        return jsonify(comments), 200
    else:
        return jsonify({"error": "댓글 목록 조회에 실패했습니다."}), 500

@comment_post_bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required # [로그인] 로그인 필수
def create_new_comment(post_id):
    """(POST) 특정 게시글에 댓글 작성 (로그인)
    
    로그인한 학생이 해당 post_id에 새 댓글을 작성합니다.
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body (JSON):
    {
        "Content": "새로운 댓글 내용입니다."
    }

    Returns:
        201 Created: {"message": "댓글이 작성되었습니다.", "Comment_ID": 2}
        400 Bad Request: {"error": "'Content'가 필요합니다."}
        500 Internal Server Error: {"error": "..."}
    """
    request_student_id = g.user['Student_ID']
    data = request.get_json()
    
    if not data or 'Content' not in data:
        return jsonify({"error": "'Content'가 필요합니다."}), 400
        
    success, result = comment_service.create_comment(post_id, request_student_id, data)
    
    if success:
        return jsonify(result), 201
    else:
        return jsonify({"error": result}), 500

# --- /api/comment/<id> ---

@comment_manage_bp.route('/<int:comment_id>', methods=['DELETE'])
@login_required # [로그인] 로그인 필수
def delete_existing_comment(comment_id):
    """(DELETE) 댓글 삭제 (로그인)
    
    로그인한 학생이 댓글을 삭제합니다.
    [권한]: 
    1. 댓글 작성자 본인
    2. 해당 동아리 관리자 (Club_Admin)
    
    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200 OK: {"message": "댓글이 성공적으로 삭제되었습니다."}
        403 Forbidden: {"error": "댓글 삭제 권한이 없습니다."}
        404 Not Found: {"error": "존재하지 않는 댓글입니다."}
    """
    request_student_id = g.user['Student_ID']
    
    success, message = comment_service.delete_comment(comment_id, request_student_id)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        if "권한" in message:
            return jsonify({"error": message}), 403
        if "존재" in message:
            return jsonify({"error": message}), 404
        return jsonify({"error": message}), 500