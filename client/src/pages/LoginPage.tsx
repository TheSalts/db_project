/**
 * 로그인 페이지
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import ErrorMessage from '../components/ErrorMessage';
import './AuthPage.css';

const LoginPage = () => {
  const [loginId, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(loginId, password);
      navigate('/');
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '로그인에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  // 입력 필드 변경 시 에러 초기화
  const handleLoginIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginId(e.target.value);
    if (error) setError('');
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (error) setError('');
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">로그인</h1>
          <p className="auth-subtitle">동아리 플랫폼에 오신 것을 환영합니다</p>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="loginId" className="form-label">
                아이디
              </label>
              <input
                id="loginId"
                type="text"
                className="input"
                value={loginId}
                onChange={handleLoginIdChange}
                placeholder="아이디를 입력하세요"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                비밀번호
              </label>
              <input
                id="password"
                type="password"
                className="input"
                value={password}
                onChange={handlePasswordChange}
                placeholder="비밀번호를 입력하세요"
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-lg auth-button"
              disabled={isLoading}
            >
              {isLoading ? '로그인 중...' : '로그인'}
            </button>
          </form>

          <p className="auth-footer">
            계정이 없으신가요?{' '}
            <Link to="/register" className="auth-link">
              회원가입
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

