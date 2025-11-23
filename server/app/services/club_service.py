# app/services/club_service.py
import pymysql # pymysql 임포트 추가
from app.utils.db import get_db_connection

def get_all_clubs(category=None):
    """
    모든 동아리 목록을 반환합니다.
    'category' 쿼리 파라미터가 있으면 필터링합니다.
    """
    conn = None
    cursor = None
    
    # 기본 SQL 쿼리
    sql = "SELECT Club_ID, Club_name, Club_Introduction, Category, Admin FROM Club"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if category:
            # 카테고리 필터가 있으면 WHERE 절 추가
            sql += " WHERE Category = %s"
            cursor.execute(sql, (category,))
        else:
            # 필터 없으면 전체 조회
            cursor.execute(sql)
            
        clubs = cursor.fetchall() # 조회된 모든 동아리 (딕셔너리 리스트)
        return clubs
        
    except Exception as e:
        print(f"동아리 목록 조회 오류: {e}")
        return None # 오류 발생 시 None 반환
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_club_by_id(club_id):
    """특정 ID의 동아리 상세 정보를 반환합니다."""
    conn = None
    cursor = None
    
    # Student 테이블과 JOIN해서 관리자(Admin)의 이름도 함께 가져옴
    sql = """
        SELECT 
            c.Club_ID, 
            c.Club_name, 
            c.Club_Introduction, 
            c.Category, 
            c.Admin,                      -- 관리자 학번 (기존 필드)
            c.Admin AS Admin_StudentID,   -- 관리자 학번 (명시적)
            s.Name AS Admin_Name          -- 관리자 이름
        FROM Club c
        LEFT JOIN Student s ON c.Admin = s.Student_ID
        WHERE c.Club_ID = %s
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(sql, (club_id,))
        club = cursor.fetchone() # 딕셔너리 형태로 1개 반환
        
        return club # club은 딕셔너리 또는 None
        
    except Exception as e:
        print(f"동아리 상세 조회 오류: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_club_info(club_id, data, request_student_id):
    """(관리자) 동아리 정보(소개, 카테고리)를 수정합니다."""
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
            return False, "동아리 정보 수정 권한이 없습니다."

        # 2. [로직] 수정할 필드 동적 생성
        fields_to_update = []
        values = []
        if 'Club_Introduction' in data:
            fields_to_update.append("Club_Introduction = %s")
            values.append(data['Club_Introduction'])
        if 'Category' in data:
            fields_to_update.append("Category = %s")
            values.append(data['Category'])

        if not fields_to_update:
            return True, "변경할 내용이 없습니다."

        # 3. [로직] 권한이 있으면 동아리 정보 UPDATE
        sql = f"UPDATE Club SET {', '.join(fields_to_update)} WHERE Club_ID = %s"
        values.append(club_id)
        
        cursor.execute(sql, tuple(values))
        conn.commit()
        
        return True, "동아리 정보가 성공적으로 수정되었습니다."

    except Exception as e:
        print(f"동아리 정보 수정 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_club_members(club_id, request_student_id):
    """(관리자) 동아리 소속 회원 목록을 조회합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] (정보 수정과 동일)
        cursor.execute("SELECT Admin FROM Club WHERE Club_ID = %s", (club_id,))
        club = cursor.fetchone()
        
        if not club:
            return None, "존재하지 않는 동아리입니다."
        if club['Admin'] != request_student_id:
            return None, "회원 목록 조회 권한이 없습니다."

        # 2. [로직] Belong 테이블과 Student 테이블 JOIN
        sql = """
            SELECT 
                b.Membership_ID,
                b.Student_ID,
                s.Name AS Student_Name,
                s.Email AS Student_Email,
                s.phone_num,
                b.Position
            FROM Belong b
            JOIN Student s ON b.Student_ID = s.Student_ID
            WHERE b.Club_ID = %s
        """
        cursor.execute(sql, (club_id,))
        members = cursor.fetchall()
        return members, "조회 성공"

    except Exception as e:
        print(f"동아리 회원 목록 조회 오류: {e}")
        return None, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def remove_club_member(membership_id, request_student_id):
    """(관리자) 동아리 회원을 강퇴(삭제)합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 이 회원(membership_id)이 속한 동아리(Club_ID)를 찾기
        sql_check = """
            SELECT b.Club_ID, c.Admin
            FROM Belong b
            JOIN Club c ON b.Club_ID = c.Club_ID
            WHERE b.Membership_ID = %s
        """
        cursor.execute(sql_check, (membership_id,))
        member_info = cursor.fetchone()

        if not member_info:
            return False, "존재하지 않는 회원 ID입니다."
        
        # 2. [권한 검증] 요청자가 그 동아리의 관리자가 맞는지 확인
        if member_info['Admin'] != request_student_id:
            return False, "회원 삭제 권한이 없습니다."
            
        # 3. [로직] 관리자 본인을 강퇴하려는지 확인
        #   (Belong 테이블에는 Admin의 학번(Student_ID)이 없음. Join 필요)
        cursor.execute("SELECT Student_ID FROM Belong WHERE Membership_ID = %s", (membership_id,))
        member_student_id = cursor.fetchone()['Student_ID']
        if member_student_id == request_student_id:
            return False, "동아리 관리자(본인)는 강퇴할 수 없습니다."

        # 4. [로직] 권한이 있으면 Belong 테이블에서 DELETE
        sql_delete = "DELETE FROM Belong WHERE Membership_ID = %s"
        cursor.execute(sql_delete, (membership_id,))
        conn.commit()
        
        return True, "회원이 성공적으로 삭제되었습니다."

    except Exception as e:
        print(f"동아리 회원 삭제 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()