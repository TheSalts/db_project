/**
 * API 통신을 위한 서비스 레이어
 */

import axios from "axios";
import type { Student, Club, Post, Application, Membership, Statistics, LoginRequest, RegisterRequest, Comment, ApplicationStatus } from "../types";

// API Base URL 설정
// VITE_API_BASE_URL 환경 변수가 있으면 사용(배포 시 등), 없으면 기본적으로 '/api' 사용 (Vite 프록시)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// 요청 인터셉터: JWT 토큰 자동 추가
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 응답 인터셉터: 401 에러 시 로그아웃 처리
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // 로그인/회원가입 API의 401 에러는 정상적인 응답이므로 리다이렉트하지 않음
        const isAuthEndpoint =
            error.config?.url?.includes("/auth/login") || error.config?.url?.includes("/auth/register");

        if (error.response?.status === 401 && !isAuthEndpoint) {
            localStorage.removeItem("token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

// ===== 인증 API =====
export const authAPI = {
    register: async (data: RegisterRequest) => {
        const response = await api.post("/auth/register", data);
        return response.data;
    },

    login: async (data: LoginRequest) => {
        const response = await api.post("/auth/login", data);
        return response.data;
    },
};

// ===== 동아리 API =====
export const clubAPI = {
    getAll: async (category?: string) => {
        const response = await api.get<Club[]>("/club", {
            params: category ? { category } : undefined,
        });
        return response.data;
    },

    getById: async (clubId: number) => {
        const response = await api.get<Club>(`/club/${clubId}`);
        return response.data;
    },

    update: async (clubId: number, data: Partial<Club>) => {
        const response = await api.put(`/club/${clubId}`, data);
        return response.data;
    },

    getMembers: async (clubId: number) => {
        const response = await api.get<Membership[]>(`/club/${clubId}/members`);
        return response.data;
    },

    removeMember: async (membershipId: number) => {
        const response = await api.delete(`/club/member/${membershipId}`);
        return response.data;
    },
};

// ===== 가입 신청 API =====
export const applyAPI = {
    submit: async (clubId: number, selfIntroduction?: string) => {
        const response = await api.post(`/apply/${clubId}`, {
            Self_Introduction: selfIntroduction,
        });
        return response.data;
    },

    getApplications: async (clubId: number) => {
        const response = await api.get<Application[]>(`/apply/manage/${clubId}`);
        return response.data;
    },

    updateStatus: async (applicationId: number, status: "승인" | "거절") => {
        const response = await api.put(`/apply/manage/${applicationId}`, {
            Status: status,
        });
        return response.data;
    },

    getStatus: async (clubId: number) => {
        const response = await api.get<ApplicationStatus>(`/apply/status/${clubId}`);
        return response.data;
    },
};

// ===== 게시글 API =====
export const postAPI = {
    getByClubId: async (clubId: number) => {
        const response = await api.get<Post[]>(`/club/${clubId}/post`);
        return response.data;
    },

    create: async (clubId: number, content: string) => {
        const response = await api.post(`/club/${clubId}/post`, {
            Content: content,
        });
        return response.data;
    },

    update: async (postId: number, content: string) => {
        const response = await api.put(`/post/${postId}`, {
            Content: content,
        });
        return response.data;
    },

    delete: async (postId: number) => {
        const response = await api.delete(`/post/${postId}`);
        return response.data;
    },
};

// ===== 마이페이지 API =====
export const mypageAPI = {
    getInfo: async () => {
        const response = await api.get<Student>("/mypage/info");
        return response.data;
    },

    updateInfo: async (data: Partial<Student>) => {
        const response = await api.put("/mypage/info", data);
        return response.data;
    },

    getApplications: async () => {
        const response = await api.get<Application[]>("/mypage/applications");
        return response.data;
    },

    getClubs: async () => {
        const response = await api.get<Membership[]>("/mypage/clubs");
        return response.data;
    },
};

// ===== 관리자 API =====
export const adminAPI = {
    getStatistics: async () => {
        const response = await api.get<Statistics>("/admin/stats");
        return response.data;
    },

    createClub: async (data: { Club_name: string; Club_Introduction?: string; Category?: string; Admin: string }) => {
        const response = await api.post("/admin/clubs", data);
        return response.data;
    },
};

// ===== 댓글 API =====
export const commentAPI = {
    getByPostId: async (postId: number) => {
        const response = await api.get<Comment[]>(`/post/${postId}/comments`);
        return response.data;
    },

    create: async (postId: number, content: string) => {
        const response = await api.post(`/post/${postId}/comment`, {
            Content: content,
        });
        return response.data;
    },

    delete: async (commentId: number) => {
        const response = await api.delete(`/comment/${commentId}`);
        return response.data;
    },
};

export default api;
