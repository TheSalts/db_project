/**
 * 동아리 상세 페이지 (정보, 게시글, 관리 탭)
 */

import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { clubAPI, postAPI, applyAPI } from "../services/api";
import { useAuth } from "../contexts/AuthContext";
import type { Club, Post, Application, Membership, ApplicationStatus } from "../types";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import "./ClubDetailPage.css";

const ClubDetailPage = () => {
    const { id } = useParams<{ id: string }>();
    const { user } = useAuth();
    const navigate = useNavigate();

    const [club, setClub] = useState<Club | null>(null);
    const [posts, setPosts] = useState<Post[]>([]);
    const [applications, setApplications] = useState<Application[]>([]);
    const [members, setMembers] = useState<Membership[]>([]);
    const [applicationStatus, setApplicationStatus] = useState<ApplicationStatus | null>(null);

    const [activeTab, setActiveTab] = useState<"info" | "posts" | "manage">("posts");
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    const [isApplying, setIsApplying] = useState(false);
    const [selfIntro, setSelfIntro] = useState("");

    const [newPost, setNewPost] = useState("");
    const [isCreatingPost, setIsCreatingPost] = useState(false);

    const clubId = parseInt(id || "0");
    const isAdmin = user && club && club.Admin_StudentID === user.Student_ID;

    useEffect(() => {
        loadClubData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id]);

    useEffect(() => {
        if (activeTab === "posts") {
            loadPosts();
        } else if (activeTab === "manage" && isAdmin) {
            loadApplications();
            loadMembers();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [activeTab]);

    const loadClubData = async () => {
        try {
            setIsLoading(true);
            const clubData = await clubAPI.getById(clubId);
            setClub(clubData);
            await loadPosts();

            // 로그인한 경우 가입 신청 상태 확인
            if (user) {
                try {
                    const status = await applyAPI.getStatus(clubId);
                    setApplicationStatus(status);
                } catch (err) {
                    console.error("가입 신청 상태 확인 실패:", err);
                }
            }
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            setError(error.response?.data?.error || "동아리 정보를 불러오는데 실패했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    const loadPosts = async () => {
        try {
            const postsData = await postAPI.getByClubId(clubId);
            setPosts(postsData);
        } catch (err) {
            console.error("게시글 로드 실패:", err);
        }
    };

    const loadApplications = async () => {
        try {
            const appsData = await applyAPI.getApplications(clubId);
            setApplications(appsData);
        } catch (err) {
            console.error("신청 목록 로드 실패:", err);
        }
    };

    const loadMembers = async () => {
        try {
            const membersData = await clubAPI.getMembers(clubId);
            setMembers(membersData);
        } catch (err) {
            console.error("회원 목록 로드 실패:", err);
        }
    };

    const handleApply = async () => {
        if (!user) {
            alert("로그인이 필요합니다.");
            navigate("/login");
            return;
        }

        try {
            setIsApplying(true);
            await applyAPI.submit(clubId, selfIntro);
            alert("가입 신청이 완료되었습니다!");
            setSelfIntro("");

            // 신청 상태 새로고침
            const status = await applyAPI.getStatus(clubId);
            setApplicationStatus(status);
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            alert(error.response?.data?.error || "가입 신청에 실패했습니다.");
        } finally {
            setIsApplying(false);
        }
    };

    const getRejectionMessage = () => {
        if (!applicationStatus?.application_date) return "";

        const rejectedDate = new Date(applicationStatus.application_date);
        const oneWeekLater = new Date(rejectedDate);
        oneWeekLater.setDate(oneWeekLater.getDate() + 7);

        const now = new Date();
        if (now >= oneWeekLater) {
            return "다시 신청할 수 있습니다.";
        }

        return `가입 신청이 거절되었습니다. ${oneWeekLater.toLocaleDateString("ko-KR")}부터 다시 신청할 수 있습니다.`;
    };

    const handleCreatePost = async () => {
        if (!newPost.trim()) return;

        try {
            setIsCreatingPost(true);
            await postAPI.create(clubId, newPost);
            setNewPost("");
            await loadPosts();
            alert("게시글이 작성되었습니다!");
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            alert(error.response?.data?.error || "게시글 작성에 실패했습니다.");
        } finally {
            setIsCreatingPost(false);
        }
    };

    const handleApplicationStatus = async (appId: number, status: "승인" | "거절") => {
        try {
            await applyAPI.updateStatus(appId, status);
            await loadApplications();
            alert(`신청이 ${status}되었습니다.`);
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            alert(error.response?.data?.error || "처리에 실패했습니다.");
        }
    };

    const handleRemoveMember = async (membershipId: number) => {
        if (!confirm("정말 강퇴하시겠습니까?")) return;

        try {
            await clubAPI.removeMember(membershipId);
            await loadMembers();
            alert("회원이 강퇴되었습니다.");
        } catch (err) {
            const error = err as { response?: { data?: { error?: string } } };
            alert(error.response?.data?.error || "강퇴에 실패했습니다.");
        }
    };

    if (isLoading) {
        return <Loading fullScreen />;
    }

    if (error || !club) {
        return (
            <div className="container">
                <ErrorMessage message={error || "동아리를 찾을 수 없습니다."} />
            </div>
        );
    }

    return (
        <div className="club-detail-page">
            <div className="container">
                <div className="club-header">
                    <div className="club-header-content">
                        <h1 className="club-title">{club.Club_name}</h1>
                        <span className="club-category-badge">{club.Category}</span>
                    </div>
                    <p className="club-description">{club.Club_Introduction || "동아리 소개가 없습니다."}</p>
                    <p className="club-admin-info">
                        관리자: {club.Admin_Name} ({club.Admin})
                    </p>
                </div>

                <div className="tabs">
                    <button
                        className={`tab ${activeTab === "posts" ? "active" : ""}`}
                        onClick={() => setActiveTab("posts")}
                    >
                        게시글
                    </button>
                    <button
                        className={`tab ${activeTab === "info" ? "active" : ""}`}
                        onClick={() => setActiveTab("info")}
                    >
                        가입 신청
                    </button>
                    {isAdmin && (
                        <button
                            className={`tab ${activeTab === "manage" ? "active" : ""}`}
                            onClick={() => setActiveTab("manage")}
                        >
                            관리
                        </button>
                    )}
                </div>

                <div className="tab-content">
                    {activeTab === "posts" && (
                        <div className="posts-tab">
                            {isAdmin && (
                                <div className="create-post-section">
                                    <h2 className="section-title">게시글 작성</h2>
                                    <textarea
                                        className="input post-textarea"
                                        placeholder="게시글 내용을 입력하세요"
                                        value={newPost}
                                        onChange={(e) => setNewPost(e.target.value)}
                                        rows={4}
                                    />
                                    <button
                                        className="btn btn-primary"
                                        onClick={handleCreatePost}
                                        disabled={isCreatingPost || !newPost.trim()}
                                    >
                                        {isCreatingPost ? "작성 중..." : "게시글 작성"}
                                    </button>
                                </div>
                            )}

                            <h2 className="section-title">게시글 목록</h2>
                            {posts.length === 0 ? (
                                <p className="empty-text">게시글이 없습니다.</p>
                            ) : (
                                <div className="posts-list">
                                    {posts.map((post) => (
                                        <div
                                            key={post.Post_ID}
                                            className="post-card clickable"
                                            onClick={() => navigate(`/clubs/${clubId}/posts/${post.Post_ID}`)}
                                        >
                                            <div className="post-header">
                                                <span className="post-author">{post.Admin_Name}</span>
                                                <span className="post-date">
                                                    {new Date(post.post_date).toLocaleDateString()}
                                                </span>
                                            </div>
                                            <p className="post-content">{post.Content}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === "info" && (
                        <div className="info-tab">
                            <div className="apply-section">
                                <h2 className="section-title">가입 신청</h2>
                                {!user ? (
                                    <p className="text-muted">
                                        가입 신청을 하려면 <a href="/login">로그인</a>이 필요합니다.
                                    </p>
                                ) : isAdmin ? (
                                    <p className="info-notice">이 동아리의 관리자입니다.</p>
                                ) : applicationStatus?.is_member ? (
                                    <p className="info-notice success">이미 이 동아리의 회원입니다.</p>
                                ) : applicationStatus?.has_applied && applicationStatus.status === "대기" ? (
                                    <p className="info-notice warning">
                                        가입 신청이 대기 중입니다. 관리자의 승인을 기다려주세요.
                                    </p>
                                ) : applicationStatus?.has_applied && applicationStatus.status === "거절" ? (
                                    <>
                                        <p className="info-notice error">{getRejectionMessage()}</p>
                                        {applicationStatus.application_date &&
                                            new Date() >=
                                                new Date(
                                                    new Date(applicationStatus.application_date).setDate(
                                                        new Date(applicationStatus.application_date).getDate() + 7
                                                    )
                                                ) && (
                                                <>
                                                    <textarea
                                                        className="input apply-textarea"
                                                        placeholder="자기소개를 입력하세요 (선택사항)"
                                                        value={selfIntro}
                                                        onChange={(e) => setSelfIntro(e.target.value)}
                                                        rows={4}
                                                    />
                                                    <button
                                                        className="btn btn-primary"
                                                        onClick={handleApply}
                                                        disabled={isApplying}
                                                    >
                                                        {isApplying ? "신청 중..." : "다시 가입 신청하기"}
                                                    </button>
                                                </>
                                            )}
                                    </>
                                ) : (
                                    <>
                                        <textarea
                                            className="input apply-textarea"
                                            placeholder="자기소개를 입력하세요 (선택사항)"
                                            value={selfIntro}
                                            onChange={(e) => setSelfIntro(e.target.value)}
                                            rows={4}
                                        />
                                        <button className="btn btn-primary" onClick={handleApply} disabled={isApplying}>
                                            {isApplying ? "신청 중..." : "가입 신청하기"}
                                        </button>
                                    </>
                                )}
                            </div>
                        </div>
                    )}

                    {activeTab === "manage" && isAdmin && (
                        <div className="manage-tab">
                            <div className="manage-section">
                                <h2 className="section-title">가입 신청 관리</h2>
                                {applications.length === 0 ? (
                                    <p className="empty-text">대기 중인 신청이 없습니다.</p>
                                ) : (
                                    <div className="applications-list">
                                        {applications.map((app) => (
                                            <div key={app.Application_ID} className="application-card">
                                                <div className="application-info">
                                                    <h3>{app.Student_Name}</h3>
                                                    <p className="text-muted">
                                                        {app.Student_ID} | {app.Student_Email}
                                                    </p>
                                                    {app.Self_Introduction && (
                                                        <p className="intro-text">{app.Self_Introduction}</p>
                                                    )}
                                                </div>
                                                <div className="application-actions">
                                                    <button
                                                        className="btn btn-sm btn-primary"
                                                        onClick={() =>
                                                            handleApplicationStatus(app.Application_ID, "승인")
                                                        }
                                                    >
                                                        승인
                                                    </button>
                                                    <button
                                                        className="btn btn-sm btn-secondary"
                                                        onClick={() =>
                                                            handleApplicationStatus(app.Application_ID, "거절")
                                                        }
                                                    >
                                                        거절
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div className="manage-section">
                                <h2 className="section-title">회원 목록</h2>
                                {members.length === 0 ? (
                                    <p className="empty-text">회원이 없습니다.</p>
                                ) : (
                                    <div className="members-list">
                                        {members.map((member) => (
                                            <div key={member.Membership_ID} className="member-card">
                                                <div className="member-info">
                                                    <h3>{member.Student_Name}</h3>
                                                    <p className="text-muted">
                                                        {member.Student_ID} | {member.Student_Email} | {member.Position}
                                                    </p>
                                                </div>
                                                {member.Student_ID !== user?.Student_ID && (
                                                    <button
                                                        className="btn btn-sm btn-secondary"
                                                        onClick={() => handleRemoveMember(member.Membership_ID)}
                                                    >
                                                        강퇴
                                                    </button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ClubDetailPage;
