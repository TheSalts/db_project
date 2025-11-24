/**
 * 사이트 관리자 통계 페이지
 */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { adminAPI } from "../services/api";
import type { Statistics } from "../types";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import "./AdminStatsPage.css";

const AdminStatsPage = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [stats, setStats] = useState<Statistics | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    const [showCreateClubModal, setShowCreateClubModal] = useState(false);
    const [clubFormData, setClubFormData] = useState({
        Club_name: "",
        Club_Introduction: "",
        Category: "사회",
        Admin: "",
    });
    const [isCreatingClub, setIsCreatingClub] = useState(false);

    useEffect(() => {
        if (!user) {
            navigate("/login");
            return;
        }

        if (user.Role !== "관리자") {
            alert("사이트 관리자만 접근할 수 있습니다.");
            navigate("/");
            return;
        }

        loadStats();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [user]);

    const loadStats = async () => {
        try {
            setIsLoading(true);
            const data = await adminAPI.getStatistics();
            setStats(data);
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            setError(error.response?.data?.error || "통계 데이터를 불러오는데 실패했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateClub = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            setIsCreatingClub(true);
            await adminAPI.createClub(clubFormData);
            alert("동아리가 생성되었습니다!");
            setShowCreateClubModal(false);
            setClubFormData({
                Club_name: "",
                Club_Introduction: "",
                Category: "학술",
                Admin: "",
            });
            await loadStats(); // 통계 갱신
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            setError(error.response?.data?.error || "동아리 생성에 실패했습니다.");
        } finally {
            setIsCreatingClub(false);
        }
    };

    if (isLoading) {
        return <Loading fullScreen />;
    }

    if (!stats) {
        return (
            <div className="container">
                <ErrorMessage message={error || "통계 데이터를 불러올 수 없습니다."} />
            </div>
        );
    }

    return (
        <div className="admin-stats-page">
            <div className="container">
                <div className="stats-header">
                    <h1 className="page-title">사이트 통계 대시보드</h1>
                    <button className="btn btn-primary" onClick={() => setShowCreateClubModal(true)}>
                        + 새 동아리 생성
                    </button>
                </div>

                {error && <ErrorMessage message={error} />}

                <div className="stats-grid">
                    <div className="stat-card stat-card-primary">
                        <div className="stat-icon">사용자</div>
                        <div className="stat-content">
                            <h3 className="stat-title">전체 학생 수</h3>
                            <p className="stat-value">{stats.total_students}명</p>
                        </div>
                    </div>

                    <div className="stat-card stat-card-success">
                        <div className="stat-icon">동아리</div>
                        <div className="stat-content">
                            <h3 className="stat-title">전체 동아리 수</h3>
                            <p className="stat-value">{stats.total_clubs}개</p>
                        </div>
                    </div>

                    <div className="stat-card stat-card-warning">
                        <div className="stat-icon">신청</div>
                        <div className="stat-content">
                            <h3 className="stat-title">대기 중인 신청</h3>
                            <p className="stat-value">{stats.pending_applications}건</p>
                        </div>
                    </div>
                </div>

                <div className="category-stats">
                    <h2 className="section-title">카테고리별 동아리 현황</h2>
                    <div className="category-grid">
                        {stats.clubs_by_category.map((category) => (
                            <div key={category.Category} className="category-card">
                                <h3 className="category-name">{category.Category}</h3>
                                <p className="category-count">{category.count}개</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {showCreateClubModal && (
                <div className="modal-overlay" onClick={() => setShowCreateClubModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">새 동아리 생성</h2>
                            <button className="modal-close" onClick={() => setShowCreateClubModal(false)}>
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleCreateClub} className="create-club-form">
                            <div className="form-group">
                                <label className="form-label">
                                    동아리명 <span className="required">*</span>
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    value={clubFormData.Club_name}
                                    onChange={(e) => setClubFormData({ ...clubFormData, Club_name: e.target.value })}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">동아리 소개</label>
                                <textarea
                                    className="input"
                                    value={clubFormData.Club_Introduction}
                                    onChange={(e) =>
                                        setClubFormData({
                                            ...clubFormData,
                                            Club_Introduction: e.target.value,
                                        })
                                    }
                                    rows={4}
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">카테고리</label>
                                <select
                                    className="input"
                                    value={clubFormData.Category}
                                    onChange={(e) => setClubFormData({ ...clubFormData, Category: e.target.value })}
                                >
                                    <option value="사회">사회</option>
                                    <option value="학술">학술</option>
                                    <option value="체육">체육</option>
                                    <option value="예술">예술</option>
                                    <option value="기타">기타</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label className="form-label">
                                    관리자 학번 <span className="required">*</span>
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    value={clubFormData.Admin}
                                    onChange={(e) => setClubFormData({ ...clubFormData, Admin: e.target.value })}
                                    placeholder="관리자로 지정할 학생의 학번"
                                    required
                                />
                            </div>

                            <div className="modal-actions">
                                <button
                                    type="button"
                                    className="btn btn-secondary"
                                    onClick={() => setShowCreateClubModal(false)}
                                >
                                    취소
                                </button>
                                <button type="submit" className="btn btn-primary" disabled={isCreatingClub}>
                                    {isCreatingClub ? "생성 중..." : "생성"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminStatsPage;
