/**
 * 에러 메시지 컴포넌트
 */

import './ErrorMessage.css';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="error-message">
      <span className="error-icon">!</span>
      <p className="error-text">{message}</p>
    </div>
  );
};

export default ErrorMessage;

