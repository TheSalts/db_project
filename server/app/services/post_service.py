# app/services/post_service.py

from app.utils.db import get_db_connection

def get_posts_by_club_id(club_id):
    """(공개) 특정 동아리의 모든 게시글 목록을 조회합니다."""
    conn = None
    cursor = None
    
    # Post 테이블과 Student 테이블을 JOIN하여 작성자(동아리 관리자) 이름도 가져옴
    sql = """
        SELECT 
            p.Post_ID,
            p.Club_ID,
            p.Content,
            p.post_date,
            s.Name AS Admin_Name
        FROM Post p
        JOIN Club c ON p.Club_ID = c.Club_ID
        JOIN Student s ON c.Admin = s.Student_ID
        WHERE p.Club_ID = %s
        ORDER BY p.post_date DESC
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (club_id,))
        posts = cursor.fetchall()
        return posts
        
    except Exception as e:
        print(f"게시글 목록 조회 오류: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def create_post(club_id, data, request_student_id):
    """(관리자) 새 게시글을 작성합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 요청자가 해당 동아리 관리자가 맞는지 확인
        cursor.execute("SELECT Admin FROM Club WHERE Club_ID = %s", (club_id,))
        club = cursor.fetchone()
        
        if not club:
            return False, "존재하지 않는 동아리입니다."
        if club['Admin'] != request_student_id:
            return False, "게시글 작성 권한이 없습니다."

        # 2. [로직] 권한이 있으면 게시글 INSERT
        sql = "INSERT INTO Post (Club_ID, Content) VALUES (%s, %s)"
        cursor.execute(sql, (club_id, data['Content']))
        conn.commit()
        
        # 방금 생성된 Post_ID를 반환하면 좋음
        new_post_id = cursor.lastrowid
        return True, {"message": "게시글이 성공적으로 작성되었습니다.", "Post_ID": new_post_id}

    except Exception as e:
        print(f"게시글 작성 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_post(post_id, data, request_student_id):
    """(관리자) 기존 게시글을 수정합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 이 게시글(post_id)이 속한 동아리의 관리자가 맞는지 확인
        sql_check = """
            SELECT c.Admin
            FROM Post p
            JOIN Club c ON p.Club_ID = c.Club_ID
            WHERE p.Post_ID = %s
        """
        cursor.execute(sql_check, (post_id,))
        post_owner = cursor.fetchone()

        if not post_owner:
            return False, "존재하지 않는 게시글입니다."
        if post_owner['Admin'] != request_student_id:
            return False, "게시글 수정 권한이 없습니다."

        # 2. [로직] 권한이 있으면 게시글 UPDATE
        sql_update = "UPDATE Post SET Content = %s WHERE Post_ID = %s"
        cursor.execute(sql_update, (data['Content'], post_id))
        conn.commit()
        
        return True, "게시글이 성공적으로 수정되었습니다."

    except Exception as e:
        print(f"게시글 수정 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_post(post_id, request_student_id):
    """(관리자) 게시글을 삭제합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] (수정과 동일)
        sql_check = """
            SELECT c.Admin
            FROM Post p
            JOIN Club c ON p.Club_ID = c.Club_ID
            WHERE p.Post_ID = %s
        """
        cursor.execute(sql_check, (post_id,))
        post_owner = cursor.fetchone()

        if not post_owner:
            return False, "존재하지 않는 게시글입니다."
        if post_owner['Admin'] != request_student_id:
            return False, "게시글 삭제 권한이 없습니다."

        # 2. [로직] 권한이 있으면 게시글 DELETE
        sql_delete = "DELETE FROM Post WHERE Post_ID = %s"
        cursor.execute(sql_delete, (post_id,))
        conn.commit()
        
        return True, "게시글이 성공적으로 삭제되었습니다."

    except Exception as e:
        print(f"게시글 삭제 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()