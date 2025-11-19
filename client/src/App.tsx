/**
 * 메인 App 컴포넌트
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ClubListPage from './pages/ClubListPage';
import ClubDetailPage from './pages/ClubDetailPage';
import MyPage from './pages/MyPage';
import AdminStatsPage from './pages/AdminStatsPage';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/clubs" element={<ClubListPage />} />
            <Route path="/clubs/:id" element={<ClubDetailPage />} />
            <Route path="/mypage" element={<MyPage />} />
            <Route path="/admin/stats" element={<AdminStatsPage />} />
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App;
