/**
 * 홈 페이지
 */

import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="container">
          <h1 className="hero-title">동아리 플랫폼</h1>
          <p className="hero-subtitle">
            다양한 동아리를 만나고, 새로운 경험을 시작하세요
          </p>
          <div className="hero-actions">
            <Link to="/clubs">
              <button className="btn btn-primary btn-lg">동아리 둘러보기</button>
            </Link>
            {!user && (
              <Link to="/register">
                <button className="btn btn-secondary btn-lg">회원가입</button>
              </Link>
            )}
          </div>
        </div>
      </div>

      <div className="features-section">
        <div className="container">
          <h2 className="section-title">주요 기능</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">검색</div>
              <h3 className="feature-title">동아리 탐색</h3>
              <p className="feature-description">
                카테고리별로 다양한 동아리를 찾아보고 상세 정보를 확인할 수 있습니다.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">글쓰기</div>
              <h3 className="feature-title">간편한 가입 신청</h3>
              <p className="feature-description">
                원하는 동아리에 클릭 한 번으로 가입 신청을 할 수 있습니다.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">그룹</div>
              <h3 className="feature-title">동아리 관리</h3>
              <p className="feature-description">
                동아리 관리자는 회원과 게시글을 손쉽게 관리할 수 있습니다.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">통계</div>
              <h3 className="feature-title">실시간 현황</h3>
              <p className="feature-description">
                내 신청 현황과 가입한 동아리 정보를 실시간으로 확인할 수 있습니다.
              </p>
            </div>
          </div>
        </div>
      </div>

      {user && (
        <div className="cta-section">
          <div className="container">
            <div className="cta-card">
              <h2 className="cta-title">
                안녕하세요, {user.Name}님!
              </h2>
              <p className="cta-description">
                새로운 동아리를 탐색하거나 마이페이지에서 활동 현황을 확인해보세요.
              </p>
              <div className="cta-actions">
                <Link to="/clubs">
                  <button className="btn btn-primary">동아리 탐색</button>
                </Link>
                <Link to="/mypage">
                  <button className="btn btn-secondary">마이페이지</button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;

