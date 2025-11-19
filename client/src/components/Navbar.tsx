/**
 * 네비게이션 바 컴포넌트
 */

import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="container navbar-content">
        <Link to="/" className="navbar-logo">
          동아리 플랫폼
        </Link>

        <div className="navbar-links">
          <Link to="/" className="navbar-link">
            홈
          </Link>
          <Link to="/clubs" className="navbar-link">
            동아리 목록
          </Link>

          {user ? (
            <>
              <Link to="/mypage" className="navbar-link">
                마이페이지
              </Link>
              {user.Role === '관리자' && (
                <Link to="/admin/stats" className="navbar-link">
                  통계
                </Link>
              )}
              <div className="navbar-user">
                <span className="navbar-username">{user.Name}</span>
                <button onClick={handleLogout} className="btn btn-sm btn-secondary">
                  로그아웃
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                로그인
              </Link>
              <Link to="/register">
                <button className="btn btn-sm btn-primary">회원가입</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

