/**
 * 로딩 스피너 컴포넌트
 */

import './Loading.css';

interface LoadingProps {
  fullScreen?: boolean;
}

const Loading = ({ fullScreen = false }: LoadingProps) => {
  if (fullScreen) {
    return (
      <div className="loading-fullscreen">
        <div className="spinner-large"></div>
        <p className="loading-text">로딩 중...</p>
      </div>
    );
  }

  return (
    <div className="loading-inline">
      <div className="spinner"></div>
    </div>
  );
};

export default Loading;

