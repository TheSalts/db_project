# app/services/apply_service.py

import pymysql
from app.utils.db import get_db_connection

def create_application(student_id, club_id, data):
    """학생이 동아리에 가입 신청을 합니다."""
    conn = None
    cursor = None
    
    sql = """
        INSERT INTO Apply (Student_ID, Club_ID, Self_Introduction)
        VALUES (%s, %s, %s)
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(sql, (
            student_id,
            club_id,
            data.get('Self_Introduction', '') # 자기소개는 선택적
        ))
        
        conn.commit()
        return True, "가입 신청이 완료되었습니다."

    except pymysql.err.IntegrityError as e:
        # UNIQUE 제약조건 위반 (UK_Student_Club_Apply)
        if e.args[0] == 1062:
            return False, "이미 해당 동아리에 가입 신청했거나 가입된 상태입니다."
        return False, "데이터베이스 오류"
        
    except Exception as e:
        print(f"가입 신청 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_applications_for_club(club_id, request_student_id):
    """(관리자용) 특정 동아리의 '대기' 중인 신청 목록 조회"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 요청한 학생이 이 동아리의 관리자가 맞는지 확인
        cursor.execute("SELECT Admin FROM Club WHERE Club_ID = %s", (club_id,))
        club = cursor.fetchone()
        
        if not club:
            return None, "존재하지 않는 동아리입니다."
        if club['Admin'] != request_student_id:
            return None, "조회 권한이 없습니다 (관리자 아님)."

        # 2. [로직] 권한이 있으면 신청자 목록 조회 (Student와 JOIN해서 이름도!)
        sql = """
            SELECT 
                a.Application_ID,
                a.Student_ID,
                s.Name AS Student_Name,
                s.Email AS Student_Email,
                a.Self_Introduction,
                a.Application_Date,
                a.Status
            FROM Apply a
            JOIN Student s ON a.Student_ID = s.Student_ID
            WHERE a.Club_ID = %s AND a.Status = '대기'
            ORDER BY a.Application_Date ASC
        """
        cursor.execute(sql, (club_id,))
        applications = cursor.fetchall()
        return applications, "조회 성공"

    except Exception as e:
        print(f"신청 목록 조회 오류: {e}")
        return None, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_application_status(application_id, status, request_student_id):
    """(관리자용) 신청 상태 변경 (승인/거절)"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 이 신청서(Application_ID)가 속한 동아리(Club_ID)를 찾기
        cursor.execute("SELECT Club_ID FROM Apply WHERE Application_ID = %s", (application_id,))
        application = cursor.fetchone()
        
        if not application:
            return False, "존재하지 않는 신청서입니다."
        
        club_id = application['Club_ID']

        # 2. [권한 검증] 요청한 학생이 그 동아리의 관리자가 맞는지 확인
        cursor.execute("SELECT Admin FROM Club WHERE Club_ID = %s", (club_id,))
        club = cursor.fetchone()

        if not club or club['Admin'] != request_student_id:
            return False, "처리 권한이 없습니다 (관리자 아님)."

        # 3. [로직] 모든 권한이 확인되면 상태 업데이트
        sql = "UPDATE Apply SET Status = %s WHERE Application_ID = %s"
        cursor.execute(sql, (status, application_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            # 여기서 status가 '승인'이면, Belong테이블에 회원 추가됨
            return True, f"신청서가 '{status}' 처리되었습니다."
        else:
            return False, "신청서 상태 변경에 실패했습니다."

    except Exception as e:
        print(f"신청 상태 변경 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_application_status(student_id, club_id):
    """학생의 특정 동아리 가입 신청 상태를 확인합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. 해당 학생의 특정 동아리 신청 상태 조회
        sql = """
            SELECT 
                Application_ID,
                Status,
                Application_Date
            FROM Apply
            WHERE Student_ID = %s AND Club_ID = %s
            ORDER BY Application_Date DESC
            LIMIT 1
        """
        cursor.execute(sql, (student_id, club_id))
        application = cursor.fetchone()
        
        if not application:
            # 신청 내역 없음
            return {"has_applied": False}, "조회 성공"
        
        # 2. Belong 테이블에서 회원 여부 확인 (승인된 경우 Belong에 추가됨)
        cursor.execute(
            "SELECT Membership_ID FROM Belong WHERE Student_ID = %s AND Club_ID = %s",
            (student_id, club_id)
        )
        membership = cursor.fetchone()
        
        return {
            "has_applied": True,
            "application_id": application['Application_ID'],
            "status": application['Status'],
            "application_date": application['Application_Date'],
            "is_member": membership is not None
        }, "조회 성공"
        
    except Exception as e:
        print(f"신청 상태 조회 오류: {e}")
        return None, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()