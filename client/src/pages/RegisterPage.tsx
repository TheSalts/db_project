/**
 * 회원가입 페이지
 */

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI } from "../services/api";
import ErrorMessage from "../components/ErrorMessage";
import "./AuthPage.css";

/**
 * 정규식 검증 함수
 */
const validateStudentID = (id: string): boolean => {
    return /^\d{11}$/.test(id);
};

const validatePhoneNumber = (phone: string): boolean => {
    return /^01[0-9]-\d{4}-\d{4}$/.test(phone);
};

const validateEmail = (email: string): boolean => {
    return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
};

const RegisterPage = () => {
    const [formData, setFormData] = useState({
        Student_ID: "",
        Login_ID: "",
        Pw: "",
        confirmPw: "",
        Name: "",
        phone_num: "",
        Email: "",
    });
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
        // 입력 필드 변경 시 에러 초기화
        if (error) setError("");
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        // 학번 형식 검증
        if (!validateStudentID(formData.Student_ID)) {
            setError("학번은 11자리 숫자여야 합니다. (예: 2024156001)");
            return;
        }

        // 전화번호 형식 검증 (입력된 경우)
        if (formData.phone_num && !validatePhoneNumber(formData.phone_num)) {
            setError("전화번호 형식이 올바르지 않습니다. (예: 010-1234-5678)");
            return;
        }

        // 이메일 형식 검증 (입력된 경우)
        if (formData.Email && !validateEmail(formData.Email)) {
            setError("이메일 형식이 올바르지 않습니다. (예: example@tukorea.ac.kr)");
            return;
        }

        // 비밀번호 확인
        if (formData.Pw !== formData.confirmPw) {
            setError("비밀번호가 일치하지 않습니다.");
            return;
        }

        setIsLoading(true);

        try {
            // confirmPw는 서버로 보내지 않음
            const registerData = {
                Student_ID: formData.Student_ID,
                Login_ID: formData.Login_ID,
                Pw: formData.Pw,
                Name: formData.Name,
                phone_num: formData.phone_num,
                Email: formData.Email,
            };
            await authAPI.register(registerData);
            alert("회원가입이 완료되었습니다!");
            navigate("/login");
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            setError(error.response?.data?.error || "회원가입에 실패했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <div className="auth-card">
                    <h1 className="auth-title">회원가입</h1>
                    <p className="auth-subtitle">동아리 플랫폼 회원이 되어보세요</p>

                    {error && <ErrorMessage message={error} />}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="Student_ID" className="form-label">
                                학번 <span className="required">*</span>
                            </label>
                            <input
                                id="Student_ID"
                                name="Student_ID"
                                type="text"
                                className="input"
                                value={formData.Student_ID}
                                onChange={handleChange}
                                placeholder="11자리 숫자 (예: 2024156001)"
                                pattern="\d{11}"
                                title="11자리 숫자를 입력하세요"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="Name" className="form-label">
                                이름 <span className="required">*</span>
                            </label>
                            <input
                                id="Name"
                                name="Name"
                                type="text"
                                className="input"
                                value={formData.Name}
                                onChange={handleChange}
                                placeholder="이름을 입력하세요"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="Login_ID" className="form-label">
                                아이디 <span className="required">*</span>
                            </label>
                            <input
                                id="Login_ID"
                                name="Login_ID"
                                type="text"
                                className="input"
                                value={formData.Login_ID}
                                onChange={handleChange}
                                placeholder="아이디를 입력하세요"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="Pw" className="form-label">
                                비밀번호 <span className="required">*</span>
                            </label>
                            <input
                                id="Pw"
                                name="Pw"
                                type="password"
                                className="input"
                                value={formData.Pw}
                                onChange={handleChange}
                                placeholder="비밀번호를 입력하세요"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="confirmPw" className="form-label">
                                비밀번호 확인 <span className="required">*</span>
                            </label>
                            <input
                                id="confirmPw"
                                name="confirmPw"
                                type="password"
                                className="input"
                                value={formData.confirmPw}
                                onChange={handleChange}
                                placeholder="비밀번호를 다시 입력하세요"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="phone_num" className="form-label">
                                연락처
                            </label>
                            <input
                                id="phone_num"
                                name="phone_num"
                                type="tel"
                                className="input"
                                value={formData.phone_num}
                                onChange={handleChange}
                                placeholder="010-1234-5678"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="Email" className="form-label">
                                이메일
                            </label>
                            <input
                                id="Email"
                                name="Email"
                                type="email"
                                className="input"
                                value={formData.Email}
                                onChange={handleChange}
                                placeholder="email@example.com"
                            />
                        </div>

                        <button type="submit" className="btn btn-primary btn-lg auth-button" disabled={isLoading}>
                            {isLoading ? "가입 중..." : "회원가입"}
                        </button>
                    </form>

                    <p className="auth-footer">
                        이미 계정이 있으신가요?{" "}
                        <Link to="/login" className="auth-link">
                            로그인
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
