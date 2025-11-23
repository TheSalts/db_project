/**
 * API 응답 및 데이터 타입 정의
 */

export interface Student {
    Student_ID: string;
    Login_ID: string;
    Name: string;
    phone_num?: string;
    Email?: string;
    Role: "일반" | "관리자";
}

export interface Club {
    Club_ID: number;
    Club_name: string;
    Club_Introduction: string;
    Category: string;
    Admin: string;
    Admin_Name?: string;
    Admin_StudentID?: string;
    Admin_Email?: string;
}

export interface Post {
    Post_ID: number;
    Club_ID: number;
    Content: string;
    post_date: string;
    Admin_Name?: string;
}

export interface Application {
    Application_ID: number;
    Club_ID: number;
    Student_ID: string;
    Self_Introduction?: string;
    Application_Date: string;
    Status: "대기" | "승인" | "거절";
    Club_name?: string;
    Student_Name?: string;
    Student_Email?: string;
}

export interface Membership {
    Membership_ID: number;
    Student_ID: string;
    Club_ID: number;
    Position: string;
    Club_name?: string;
    Category?: string;
    Student_Name?: string;
    Student_Email?: string;
    phone_num?: string;
}

export interface Comment {
    Comment_ID: number;
    Post_ID: number;
    Student_ID: string;
    Student_Name?: string;
    Content: string;
    created_at: string;
}

export interface ApplicationStatus {
    has_applied: boolean;
    application_id?: number;
    status?: "대기" | "승인" | "거절";
    application_date?: string;
    is_member?: boolean;
}

export interface Statistics {
    total_students: number;
    total_clubs: number;
    pending_applications: number;
    clubs_by_category: Array<{
        Category: string;
        count: number;
    }>;
}

export interface AuthContextType {
    user: Student | null;
    token: string | null;
    login: (loginId: string, password: string) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
}

export interface LoginRequest {
    Login_ID: string;
    Pw: string;
}

export interface RegisterRequest {
    Student_ID: string;
    Login_ID: string;
    Pw: string;
    Name: string;
    phone_num?: string;
    Email?: string;
}

export interface ApiError {
    error: string;
}

export interface ApiSuccess {
    message: string;
}
