/**
 * 게시글 상세 페이지 (게시글 내용 + 댓글)
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { postAPI, commentAPI, clubAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import type { Post, Comment, Club } from '../types';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import './PostDetailPage.css';

const PostDetailPage = () => {
  const { clubId, postId } = useParams<{ clubId: string; postId: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [post, setPost] = useState<Post | null>(null);
  const [club, setClub] = useState<Club | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  const parsedPostId = parseInt(postId || '0');
  const parsedClubId = parseInt(clubId || '0');
  const isAdmin = user && club && club.Admin_StudentID === user.Student_ID;

  useEffect(() => {
    loadPostData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  const loadPostData = async () => {
    try {
      setIsLoading(true);
      const postsData = await postAPI.getByClubId(parsedClubId);
      const currentPost = postsData.find((p: Post) => p.Post_ID === parsedPostId);
      
      if (!currentPost) {
        setError('게시글을 찾을 수 없습니다.');
        return;
      }
      
      setPost(currentPost);
      
      const clubData = await clubAPI.getById(parsedClubId);
      setClub(clubData);
      
      await loadComments();
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || '게시글을 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const commentsData = await commentAPI.getByPostId(parsedPostId);
      setComments(commentsData);
    } catch (err) {
      console.error('댓글 로드 실패:', err);
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user) {
      alert('댓글을 작성하려면 로그인이 필요합니다.');
      navigate('/login');
      return;
    }

    if (!newComment.trim()) {
      alert('댓글 내용을 입력해주세요.');
      return;
    }

    try {
      setIsSubmittingComment(true);
      await commentAPI.create(parsedPostId, newComment);
      setNewComment('');
      await loadComments();
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      alert(error.response?.data?.error || '댓글 작성에 실패했습니다.');
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('댓글을 삭제하시겠습니까?')) return;

    try {
      await commentAPI.delete(commentId);
      await loadComments();
      alert('댓글이 삭제되었습니다.');
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      alert(error.response?.data?.error || '댓글 삭제에 실패했습니다.');
    }
  };

  const handleDeletePost = async () => {
    if (!confirm('게시글을 삭제하시겠습니까?')) return;

    try {
      await postAPI.delete(parsedPostId);
      alert('게시글이 삭제되었습니다.');
      navigate(`/clubs/${parsedClubId}`);
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      alert(error.response?.data?.error || '게시글 삭제에 실패했습니다.');
    }
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  if (error || !post || !club) {
    return (
      <div className="container">
        <ErrorMessage message={error || '게시글을 찾을 수 없습니다.'} />
        <button className="btn btn-secondary" onClick={() => navigate(`/clubs/${parsedClubId}`)}>
          동아리로 돌아가기
        </button>
      </div>
    );
  }

  return (
    <div className="post-detail-page">
      <div className="container">
        <button className="btn btn-secondary back-btn" onClick={() => navigate(`/clubs/${parsedClubId}`)}>
          ← 목록으로
        </button>

        <div className="post-detail-card">
          <div className="post-header">
            <div className="post-meta">
              <span className="post-author">{post.Admin_Name || '관리자'}</span>
              <span className="post-date">
                {new Date(post.post_date).toLocaleString('ko-KR')}
              </span>
            </div>
            {isAdmin && (
              <button className="btn btn-sm btn-secondary" onClick={handleDeletePost}>
                삭제
              </button>
            )}
          </div>
          <div className="post-content">
            {post.Content}
          </div>
        </div>

        <div className="comments-section">
          <h2 className="section-title">댓글 ({comments.length})</h2>
          
          {user ? (
            <form className="comment-form" onSubmit={handleSubmitComment}>
              <textarea
                className="input comment-textarea"
                placeholder="댓글을 입력하세요"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                rows={3}
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmittingComment || !newComment.trim()}
              >
                {isSubmittingComment ? '작성 중...' : '댓글 작성'}
              </button>
            </form>
          ) : (
            <div className="comment-login-notice">
              댓글을 작성하려면 <a href="/login">로그인</a>이 필요합니다.
            </div>
          )}

          <div className="comments-list">
            {comments.length === 0 ? (
              <p className="empty-text">댓글이 없습니다.</p>
            ) : (
              comments.map((comment) => (
                <div key={comment.Comment_ID} className="comment-card">
                  <div className="comment-header">
                    <div className="comment-meta">
                      <span className="comment-author">{comment.Student_Name}</span>
                      <span className="comment-date">
                        {new Date(comment.created_at).toLocaleString('ko-KR')}
                      </span>
                    </div>
                    {(user?.Student_ID === comment.Student_ID || isAdmin) && (
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={() => handleDeleteComment(comment.Comment_ID)}
                      >
                        삭제
                      </button>
                    )}
                  </div>
                  <p className="comment-content">{comment.Content}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetailPage;

