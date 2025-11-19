/**
 * 동아리 목록 페이지
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { clubAPI } from '../services/api';
import type { Club } from '../types';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import './ClubListPage.css';

const CATEGORIES = ['전체', '사회', '학술', '체육', '예술', '기타'];

const ClubListPage = () => {
  const [clubs, setClubs] = useState<Club[]>([]);
  const [filteredClubs, setFilteredClubs] = useState<Club[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('전체');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadClubs();
  }, []);

  useEffect(() => {
    if (selectedCategory === '전체') {
      setFilteredClubs(clubs);
    } else {
      setFilteredClubs(clubs.filter((club) => club.Category === selectedCategory));
    }
  }, [selectedCategory, clubs]);

  const loadClubs = async () => {
    try {
      setIsLoading(true);
      const data = await clubAPI.getAll();
      setClubs(data);
      setFilteredClubs(data);
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '동아리 목록을 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="club-list-page">
      <div className="container">
        <div className="page-header">
          <h1 className="page-title">동아리 목록</h1>
          <p className="page-description">
            다양한 카테고리의 동아리를 탐색하고 관심있는 동아리에 가입해보세요
          </p>
        </div>

        {error && <ErrorMessage message={error} />}

        <div className="category-filter">
          {CATEGORIES.map((category) => (
            <button
              key={category}
              className={`category-btn ${
                selectedCategory === category ? 'active' : ''
              }`}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>

        {filteredClubs.length === 0 ? (
          <div className="empty-state">
            <p className="empty-text">해당 카테고리의 동아리가 없습니다.</p>
          </div>
        ) : (
          <div className="clubs-grid">
            {filteredClubs.map((club) => (
              <Link
                key={club.Club_ID}
                to={`/clubs/${club.Club_ID}`}
                className="club-card-link"
              >
                <div className="club-card">
                  <div className="club-card-header">
                    <h3 className="club-name">{club.Club_name}</h3>
                    <span className="club-category">{club.Category}</span>
                  </div>
                  <p className="club-intro">
                    {club.Club_Introduction || '동아리 소개가 없습니다.'}
                  </p>
                  <div className="club-card-footer">
                    <span className="club-admin">관리자: {club.Admin}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ClubListPage;

