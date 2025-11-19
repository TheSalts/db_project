/**
 * 인증 상태 관리를 위한 Context
 */

import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import { authAPI, mypageAPI } from "../services/api";
import type { AuthContextType, Student } from "../types";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<Student | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // 초기 로드: localStorage에서 토큰 확인
    useEffect(() => {
        const loadUser = async () => {
            const savedToken = localStorage.getItem("token");
            if (savedToken) {
                setToken(savedToken);
                try {
                    // 토큰이 있으면 사용자 정보 가져오기
                    const userData = await mypageAPI.getInfo();
                    setUser(userData);
                } catch (error) {
                    // 토큰이 유효하지 않으면 제거
                    localStorage.removeItem("token");
                    setToken(null);
                }
            }
            setIsLoading(false);
        };

        loadUser();
    }, []);

    const login = async (loginId: string, password: string) => {
        const response = await authAPI.login({
            Login_ID: loginId,
            Pw: password,
        });

        const { token: newToken } = response;
        localStorage.setItem("token", newToken);
        setToken(newToken);

        // 로그인 후 사용자 정보 가져오기
        const userData = await mypageAPI.getInfo();
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
    };

    return <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
