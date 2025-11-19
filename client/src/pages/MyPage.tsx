/**
 * 마이페이지 (내 정보, 가입 신청 현황, 가입한 동아리)
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { mypageAPI } from '../services/api';
import type { Application, Membership } from '../types';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import './MyPage.css';

const MyPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState<'info' | 'applications' | 'clubs'>('info');
  const [applications, setApplications] = useState<Application[]>([]);
  const [clubs, setClubs] = useState<Membership[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    Name: '',
    phone_num: '',
    Email: '',
    Pw: '',
    confirmPw: '',
  });

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    // 사용자 정보로 폼 초기화
    setFormData({
      Name: user.Name,
      phone_num: user.phone_num || '',
      Email: user.Email || '',
      Pw: '',
      confirmPw: '',
    });
  }, [user]);

  useEffect(() => {
    if (activeTab === 'applications') {
      loadApplications();
    } else if (activeTab === 'clubs') {
      loadClubs();
    }
  }, [activeTab]);

  const loadApplications = async () => {
    try {
      setIsLoading(true);
      const data = await mypageAPI.getApplications();
      setApplications(data);
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '신청 현황을 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const loadClubs = async () => {
    try {
      setIsLoading(true);
      const data = await mypageAPI.getClubs();
      setClubs(data);
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '동아리 목록을 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateInfo = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // 비밀번호 변경 시 확인
    if (formData.Pw && formData.Pw !== formData.confirmPw) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
    }

    try {
      const updateData: any = {
        Name: formData.Name,
        phone_num: formData.phone_num,
        Email: formData.Email,
      };

      if (formData.Pw) {
        updateData.Pw = formData.Pw;
      }

      await mypageAPI.updateInfo(updateData);
      alert('정보가 수정되었습니다!');
      setIsEditing(false);
      
      // 로그아웃 후 재로그인
      logout();
      navigate('/login');
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '정보 수정에 실패했습니다.');
    }
  };

  if (!user) {
    return null;
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case '승인':
        return 'status-approved';
      case '거절':
        return 'status-rejected';
      default:
        return 'status-pending';
    }
  };

  return (
    <div className="mypage">
      <div className="container">
        <div className="mypage-header">
          <h1 className="page-title">마이페이지</h1>
          <p className="page-description">
            {user.Name}님의 정보와 활동 현황을 관리할 수 있습니다
          </p>
        </div>

        {error && <ErrorMessage message={error} />}

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'info' ? 'active' : ''}`}
            onClick={() => setActiveTab('info')}
          >
            내 정보
          </button>
          <button
            className={`tab ${activeTab === 'applications' ? 'active' : ''}`}
            onClick={() => setActiveTab('applications')}
          >
            가입 신청 현황
          </button>
          <button
            className={`tab ${activeTab === 'clubs' ? 'active' : ''}`}
            onClick={() => setActiveTab('clubs')}
          >
            가입한 동아리
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'info' && (
            <div className="info-tab">
              <div className="info-card">
                <div className="info-header">
                  <h2 className="section-title">내 정보</h2>
                  {!isEditing && (
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => setIsEditing(true)}
                    >
                      수정
                    </button>
                  )}
                </div>

                {isEditing ? (
                  <form onSubmit={handleUpdateInfo} className="edit-form">
                    <div className="form-group">
                      <label className="form-label">학번</label>
                      <input
                        type="text"
                        className="input"
                        value={user.Student_ID}
                        disabled
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label">아이디</label>
                      <input
                        type="text"
                        className="input"
                        value={user.Login_ID}
                        disabled
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label">이름</label>
                      <input
                        type="text"
                        className="input"
                        value={formData.Name}
                        onChange={(e) =>
                          setFormData({ ...formData, Name: e.target.value })
                        }
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label">연락처</label>
                      <input
                        type="tel"
                        className="input"
                        value={formData.phone_num}
                        onChange={(e) =>
                          setFormData({ ...formData, phone_num: e.target.value })
                        }
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label">이메일</label>
                      <input
                        type="email"
                        className="input"
                        value={formData.Email}
                        onChange={(e) =>
                          setFormData({ ...formData, Email: e.target.value })
                        }
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label">새 비밀번호 (선택사항)</label>
                      <input
                        type="password"
                        className="input"
                        value={formData.Pw}
                        onChange={(e) =>
                          setFormData({ ...formData, Pw: e.target.value })
                        }
                        placeholder="변경하지 않으려면 비워두세요"
                      />
                    </div>

                    {formData.Pw && (
                      <div className="form-group">
                        <label className="form-label">비밀번호 확인</label>
                        <input
                          type="password"
                          className="input"
                          value={formData.confirmPw}
                          onChange={(e) =>
                            setFormData({ ...formData, confirmPw: e.target.value })
                          }
                        />
                      </div>
                    )}

                    <div className="form-actions">
                      <button type="submit" className="btn btn-primary">
                        저장
                      </button>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => setIsEditing(false)}
                      >
                        취소
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="info-display">
                    <div className="info-item">
                      <span className="info-label">학번:</span>
                      <span className="info-value">{user.Student_ID}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">아이디:</span>
                      <span className="info-value">{user.Login_ID}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">이름:</span>
                      <span className="info-value">{user.Name}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">연락처:</span>
                      <span className="info-value">{user.phone_num || '-'}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">이메일:</span>
                      <span className="info-value">{user.Email || '-'}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">권한:</span>
                      <span className="info-value">{user.Role}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'applications' && (
            <div className="applications-tab">
              {isLoading ? (
                <Loading />
              ) : applications.length === 0 ? (
                <p className="empty-text">가입 신청 내역이 없습니다.</p>
              ) : (
                <div className="applications-list">
                  {applications.map((app) => (
                    <div key={app.Application_ID} className="application-card">
                      <div className="application-header">
                        <h3 className="club-name">{app.Club_name}</h3>
                        <span className={`status-badge ${getStatusColor(app.Status)}`}>
                          {app.Status}
                        </span>
                      </div>
                      <p className="application-date">
                        신청일: {new Date(app.Application_Date).toLocaleDateString()}
                      </p>
                      {app.Self_Introduction && (
                        <p className="application-intro">{app.Self_Introduction}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'clubs' && (
            <div className="clubs-tab">
              {isLoading ? (
                <Loading />
              ) : clubs.length === 0 ? (
                <p className="empty-text">가입한 동아리가 없습니다.</p>
              ) : (
                <div className="clubs-grid">
                  {clubs.map((membership) => (
                    <Link
                      key={membership.Membership_ID}
                      to={`/clubs/${membership.Club_ID}`}
                      className="club-link"
                    >
                      <div className="club-card">
                        <div className="club-card-header">
                          <h3 className="club-name">{membership.Club_name}</h3>
                          <span className="club-category">{membership.Category}</span>
                        </div>
                        <p className="club-position">직책: {membership.Position}</p>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MyPage;

