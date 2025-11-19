# app/services/comment_service.py

from app.utils.db import get_db_connection

def get_comments_for_post(post_id):
    """(공개) 특정 게시글의 모든 댓글을 조회합니다."""
    conn = None
    cursor = None
    
    # Student와 JOIN하여 댓글 작성자 이름(Student_Name)도 가져옴
    sql = """
        SELECT 
            c.Comment_ID,
            c.Post_ID,
            c.Student_ID,
            s.Name AS Student_Name,
            c.Content,
            c.created_at
        FROM Comment c
        JOIN Student s ON c.Student_ID = s.Student_ID
        WHERE c.Post_ID = %s
        ORDER BY c.created_at ASC
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (post_id,))
        comments = cursor.fetchall()
        return comments
        
    except Exception as e:
        print(f"댓글 목록 조회 오류: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def create_comment(post_id, student_id, data):
    """(로그인) 특정 게시글에 새 댓글을 작성합니다."""
    conn = None
    cursor = None
    
    sql = "INSERT INTO Comment (Post_ID, Student_ID, Content) VALUES (%s, %s, %s)"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (post_id, student_id, data['Content']))
        conn.commit()
        
        # 방금 생성된 Comment_ID 반환
        new_comment_id = cursor.lastrowid
        return True, {"message": "댓글이 작성되었습니다.", "Comment_ID": new_comment_id}

    except Exception as e:
        print(f"댓글 작성 오류: {e}")
        return False, "댓글 작성 중 오류가 발생했습니다."
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_comment(comment_id, request_student_id):
    """(로그인) 댓글을 삭제합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증 1] 이 댓글(comment_id)의 작성자(Student_ID)를 찾기
        sql_check = """
            SELECT 
                c.Student_ID,   -- 댓글 작성자
                cl.Admin AS Club_Admin -- 이 댓글이 달린 글의 동아리 관리자
            FROM Comment c
            JOIN Post p ON c.Post_ID = p.Post_ID
            JOIN Club cl ON p.Club_ID = cl.Club_ID
            WHERE c.Comment_ID = %s
        """
        cursor.execute(sql_check, (comment_id,))
        comment_info = cursor.fetchone()

        if not comment_info:
            return False, "존재하지 않는 댓글입니다."

        # 2. [권한 검증 2] 요청자가 (댓글 작성자) 또는 (동아리 관리자)인지 확인
        comment_author_id = comment_info['Student_ID']
        club_admin_id = comment_info['Club_Admin']

        if request_student_id != comment_author_id and request_student_id != club_admin_id:
            return False, "댓글 삭제 권한이 없습니다."

        # 3. [로직] 권한이 있으면 DELETE
        sql_delete = "DELETE FROM Comment WHERE Comment_ID = %s"
        cursor.execute(sql_delete, (comment_id,))
        conn.commit()
        
        return True, "댓글이 성공적으로 삭제되었습니다."

    except Exception as e:
        print(f"댓글 삭제 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()