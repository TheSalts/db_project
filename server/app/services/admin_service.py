# app/services/admin_service.py

from app.utils.db import get_db_connection

def get_site_statistics(request_student_id):
    """(사이트 관리자) 전체 사이트 통계를 반환합니다."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 요청자의 Role이 '관리자'가 맞는지 확인
        cursor.execute("SELECT Role FROM Student WHERE Student_ID = %s", (request_student_id,))
        user_role = cursor.fetchone()
        
        if not user_role or user_role['Role'] != '관리자':
            return None, "통계 조회 권한이 없습니다 (사이트 관리자 아님)."

        # 2. [로직] 전체 학생 수
        cursor.execute("SELECT COUNT(*) AS total_students FROM Student")
        total_students = cursor.fetchone()['total_students']
        
        # 3. [로직] 전체 동아리 수
        cursor.execute("SELECT COUNT(*) AS total_clubs FROM Club")
        total_clubs = cursor.fetchone()['total_clubs']
        
        # 4. [로직] 카테고리별 동아리 수 (GROUP BY)
        cursor.execute("""
            SELECT Category, COUNT(*) AS count 
            FROM Club 
            GROUP BY Category
        """)
        clubs_by_category = cursor.fetchall() # [{'Category': '학술', 'count': 5}, ...]

        # 5. [로직] (추가) 최근 가입 신청 수 (예: '대기' 상태)
        cursor.execute("SELECT COUNT(*) AS pending_applications FROM Apply WHERE Status = '대기'")
        pending_applications = cursor.fetchone()['pending_applications']

        # 최종 통계 데이터 조립
        statistics = {
            "total_students": total_students,
            "total_clubs": total_clubs,
            "pending_applications": pending_applications,
            "clubs_by_category": clubs_by_category
        }
        
        return statistics, "조회 성공"

    except Exception as e:
        print(f"통계 조회 오류: {e}")
        return None, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def create_club(data, request_student_id):
    """
    (사이트 관리자) 새 동아리를 생성합니다.
    
    Args:
        data: 동아리 정보 (Club_name, Club_Introduction, Category, Admin)
        request_student_id: 요청자 학번
    
    Returns:
        (success: bool, message/club_id: str/int)
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. [권한 검증] 요청자의 Role이 '관리자'가 맞는지 확인
        cursor.execute("SELECT Role FROM Student WHERE Student_ID = %s", (request_student_id,))
        user_role = cursor.fetchone()
        
        if not user_role or user_role['Role'] != '관리자':
            return False, "동아리 생성 권한이 없습니다 (사이트 관리자 아님)."

        # 2. [검증] 필수 필드 확인
        required_fields = ['Club_name', 'Admin']
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"'{field}' 필드는 필수입니다."

        # 3. [검증] Admin(관리자 학번)이 실제로 존재하는지 확인
        cursor.execute("SELECT Student_ID FROM Student WHERE Student_ID = %s", (data['Admin'],))
        admin_exists = cursor.fetchone()
        if not admin_exists:
            return False, "존재하지 않는 학번입니다. 관리자(Admin)는 등록된 학생이어야 합니다."

        # 4. [로직] 동아리 INSERT
        sql = """
            INSERT INTO Club (Club_name, Club_Introduction, Category, Admin)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data['Club_name'],
            data.get('Club_Introduction', ''),
            data.get('Category', '기타'),
            data['Admin']
        ))
        conn.commit()
        
        # 생성된 동아리 ID 반환
        club_id = cursor.lastrowid
        
        return True, club_id

    except Exception as e:
        print(f"동아리 생성 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()