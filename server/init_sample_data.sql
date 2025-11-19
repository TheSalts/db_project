-- 한국공학대학교 동아리 플랫폼 초기 샘플 데이터
-- init_db.py 실행 후에 이 파일을 실행하세요.

USE `club_db`;

-- 샘플 학생 데이터 (관리자 포함)
-- 사이트 관리자
INSERT INTO `Student` (`Student_ID`, `Login_ID`, `Pw`, `Name`, `phone_num`, `Email`, `Role`) VALUES
('20240001', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김관리', '010-1234-5678', 'admin@tukorea.ac.kr', '관리자');

-- 동아리 관리자들 (사회분과)
INSERT INTO `Student` (`Student_ID`, `Login_ID`, `Pw`, `Name`, `phone_num`, `Email`, `Role`) VALUES
('20240101', 'nanum_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '최봉사', '010-1111-1111', 'nanum@tukorea.ac.kr', '일반'),
('20240102', 'rotaract_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김로타', '010-1111-2222', 'rotaract@tukorea.ac.kr', '일반'),
('20240103', 'masil_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '이마실', '010-1111-3333', 'masil@tukorea.ac.kr', '일반'),
('20240104', 'ccc_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '박씨씨', '010-1111-4444', 'ccc@tukorea.ac.kr', '일반'),
('20240105', 'ouiparfum_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '정향수', '010-1111-5555', 'ouiparfum@tukorea.ac.kr', '일반'),
('20240106', 'thetiki_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '강티키', '010-1111-6666', 'thetiki@tukorea.ac.kr', '일반');

-- 동아리 관리자들 (학술분과)
INSERT INTO `Student` (`Student_ID`, `Login_ID`, `Pw`, `Name`, `phone_num`, `Email`, `Role`) VALUES
('20240111', 'seabueong_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김알고', '010-2222-1111', 'seabueong@tukorea.ac.kr', '일반'),
('20240112', 'aram_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '이아람', '010-2222-2222', 'aram@tukorea.ac.kr', '일반'),
('20240113', 'teamnc_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '박엔써', '010-2222-3333', 'teamnc@tukorea.ac.kr', '일반'),
('20240114', 'hyeium_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '최혜윰', '010-2222-4444', 'hyeium@tukorea.ac.kr', '일반'),
('20240115', 'cir_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '정써클', '010-2222-5555', 'cir@tukorea.ac.kr', '일반'),
('20240116', 'ham_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '강햄', '010-2222-6666', 'ham@tukorea.ac.kr', '일반');

-- 동아리 관리자들 (체육분과)
INSERT INTO `Student` (`Student_ID`, `Login_ID`, `Pw`, `Name`, `phone_num`, `Email`, `Role`) VALUES
('20240121', 'dungkids_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김덩크', '010-3333-1111', 'dungkids@tukorea.ac.kr', '일반'),
('20240122', 'sansaram_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '이등산', '010-3333-2222', 'sansaram@tukorea.ac.kr', '일반'),
('20240123', 'santakgu_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '박탁구', '010-3333-3333', 'santakgu@tukorea.ac.kr', '일반'),
('20240124', 'seoseong_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '최서핑', '010-3333-4444', 'seoseong@tukorea.ac.kr', '일반'),
('20240125', 'winners_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '정승리', '010-3333-5555', 'winners@tukorea.ac.kr', '일반'),
('20240126', 'teamfight_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '강파이', '010-3333-6666', 'teamfight@tukorea.ac.kr', '일반'),
('20240127', 'insane_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김인세', '010-3333-7777', 'insane@tukorea.ac.kr', '일반'),
('20240128', 'wing_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '이윙', '010-3333-8888', 'wing@tukorea.ac.kr', '일반');

-- 일반 학생들
INSERT INTO `Student` (`Student_ID`, `Login_ID`, `Pw`, `Name`, `phone_num`, `Email`, `Role`) VALUES
('20240201', 'student01', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '김학생', '010-1234-0001', 'student01@tukorea.ac.kr', '일반'),
('20240202', 'student02', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '이학생', '010-1234-0002', 'student02@tukorea.ac.kr', '일반'),
('20240203', 'student03', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '박학생', '010-1234-0003', 'student03@tukorea.ac.kr', '일반'),
('20240204', 'student04', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '최학생', '010-1234-0004', 'student04@tukorea.ac.kr', '일반'),
('20240205', 'student05', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Y5KAQoYL6d3u', '정학생', '010-1234-0005', 'student05@tukorea.ac.kr', '일반');

-- 비밀번호: 모두 'password123' (bcrypt 해시)

-- 동아리 데이터 (한국공학대학교 실제 동아리)
-- 사회분과
INSERT INTO `Club` (`Club_name`, `Club_Introduction`, `Category`, `Admin`) VALUES
('나눔', '지역 사회를 위한 다양한 봉사 활동을 진행하는 동아리입니다. 환경 보호를 위한 플로깅, 독거노인 돕기 등 다양한 활동을 합니다.', '사회', '20240101'),
('로타랙트', '국제 로타리의 청년 봉사 동아리입니다. 지역사회 봉사와 국제 교류 활동을 통해 리더십을 함양합니다.', '사회', '20240102'),
('마실', '지역 사회와 함께하는 사회봉사 동아리입니다. 다양한 사회 공헌 활동으로 따뜻한 세상을 만들어갑니다.', '사회', '20240103'),
('CCC', 'Campus Crusade for Christ - 기독교 대학 선교 동아리입니다. 신앙 성장과 캠퍼스 복음 전파를 목표로 합니다.', '사회', '20240104'),
('Oui Parfum', '향수와 향에 대한 관심을 공유하는 동아리입니다. 향수 제작과 조향 체험을 통해 향의 세계를 탐구합니다.', '사회', '20240105'),
('The Tiki', '칵테일과 바텐딩을 배우고 즐기는 동아리입니다. 다양한 칵테일 제조 기술을 익히고 파티 문화를 만들어갑니다.', '사회', '20240106');

-- 학술분과
INSERT INTO `Club` (`Club_name`, `Club_Introduction`, `Category`, `Admin`) VALUES
('씨부엉', '알고리즘 및 프로그래밍 문제 해결을 중심으로 활동하는 코딩 동아리입니다. 코딩 테스트 준비와 알고리즘 공부를 함께합니다.', '학술', '20240111'),
('아람', '한국어와 한국 문화를 탐구하는 학술 동아리입니다. 독서 토론과 글쓰기 활동을 통해 교양을 쌓습니다.', '학술', '20240112'),
('팀엔써', 'Team&C - 협업과 창의적 문제 해결 능력을 키우는 학술 동아리입니다. 다양한 프로젝트를 통해 실무 역량을 향상시킵니다.', '학술', '20240113'),
('혜윰', '토론과 사색을 즐기는 인문학 동아리입니다. 철학, 역사, 문학 등 다양한 주제로 깊이 있는 대화를 나눕니다.', '학술', '20240114'),
('CIR', 'Circle of Innovation & Research - 혁신과 연구를 추구하는 학술 동아리입니다. 최신 기술 트렌드를 연구하고 공유합니다.', '학술', '20240115'),
('HAM', '아마추어 무선 통신 동아리입니다. 무선 통신 기술을 배우고 실제 무선 교신 활동을 진행합니다.', '학술', '20240116');

-- 체육분과
INSERT INTO `Club` (`Club_name`, `Club_Introduction`, `Category`, `Admin`) VALUES
('덩키즈', '농구를 사랑하는 학생들의 동아리입니다. 덩크슛의 꿈을 향해 함께 성장하며 대학 리그에 참가합니다.', '체육', '20240121'),
('산사람', '등산과 야외 활동을 즐기는 동아리입니다. 전국의 명산을 오르며 자연과 하나되는 경험을 합니다.', '체육', '20240122'),
('산탁구', '탁구를 통해 건강과 우정을 키우는 동아리입니다. 초보자부터 상급자까지 모두 환영하며 함께 실력을 키워갑니다.', '체육', '20240123'),
('서성', '서핑과 보드 스포츠를 즐기는 동아리입니다. 파도 위에서의 자유와 스릴을 함께 느낍니다.', '체육', '20240124'),
('위너스', '배드민턴 동아리입니다. 승리를 향한 열정으로 함께 훈련하며 각종 대회에 출전합니다.', '체육', '20240125'),
('팀파이트', '격투기와 무술을 배우는 동아리입니다. 체력 단련과 호신술을 익히며 정신력을 키웁니다.', '체육', '20240126'),
('INSANE', '인라인 스케이트와 익스트림 스포츠를 즐기는 동아리입니다. 도전적이고 역동적인 활동을 추구합니다.', '체육', '20240127'),
('WING', '배드민턴과 스쿼시를 즐기는 동아리입니다. 날아오르는 셔틀콕처럼 함께 성장합니다.', '체육', '20240128');

-- 초기 소속 데이터 (각 동아리 관리자들은 자신의 동아리 회원)
-- 사회분과
INSERT INTO `Belong` (`Student_ID`, `Club_ID`, `Position`) VALUES
('20240101', 1, '회장'),
('20240102', 2, '회장'),
('20240103', 3, '회장'),
('20240104', 4, '회장'),
('20240105', 5, '회장'),
('20240106', 6, '회장');

-- 학술분과
INSERT INTO `Belong` (`Student_ID`, `Club_ID`, `Position`) VALUES
('20240111', 7, '회장'),
('20240112', 8, '회장'),
('20240113', 9, '회장'),
('20240114', 10, '회장'),
('20240115', 11, '회장'),
('20240116', 12, '회장');

-- 체육분과
INSERT INTO `Belong` (`Student_ID`, `Club_ID`, `Position`) VALUES
('20240121', 13, '회장'),
('20240122', 14, '회장'),
('20240123', 15, '회장'),
('20240124', 16, '회장'),
('20240125', 17, '회장'),
('20240126', 18, '회장'),
('20240127', 19, '회장'),
('20240128', 20, '회장');

-- 일부 학생들의 동아리 가입
INSERT INTO `Belong` (`Student_ID`, `Club_ID`, `Position`) VALUES
('20240201', 1, '일반회원'),
('20240201', 7, '일반회원'),
('20240202', 2, '일반회원'),
('20240202', 13, '일반회원'),
('20240203', 14, '일반회원'),
('20240203', 7, '일반회원'),
('20240204', 17, '일반회원'),
('20240205', 13, '일반회원');

-- 샘플 게시글
-- 사회분과 게시글
INSERT INTO `Post` (`Club_ID`, `Content`, `post_date`) VALUES
(1, '안녕하세요! 나눔 동아리입니다. 이번 주 일요일 플로깅 활동 예정입니다. 환경 보호에 동참해주세요!', NOW() - INTERVAL 1 DAY),
(1, '나눔 동아리 이번 학기 신입 부원을 모집합니다. 함께 따뜻한 세상을 만들어갈 분들을 기다립니다!', NOW() - INTERVAL 5 DAY),
(2, '로타랙트 동아리 정기 모임 안내입니다. 다음 주 목요일 오후 6시에 있을 예정입니다.', NOW() - INTERVAL 3 DAY),
(4, 'CCC 동아리 성경 공부 모임을 시작합니다. 매주 수요일 저녁 7시에 모여요!', NOW() - INTERVAL 4 DAY);

-- 학술분과 게시글
INSERT INTO `Post` (`Club_ID`, `Content`, `post_date`) VALUES
(7, '씨부엉 동아리 알고리즘 스터디 모집 공지입니다. 백준, 프로그래머스 문제를 함께 풀어봅시다!', NOW() - INTERVAL 4 DAY),
(7, '다음 주 월요일 오후 6시에 정기 세미나가 있습니다. 주제는 "알고리즘 문제 풀이 전략"입니다.', NOW() - INTERVAL 2 DAY),
(8, '아람 동아리 이번 달 독서 토론 주제는 "사피엔스"입니다. 많은 관심 부탁드려요!', NOW() - INTERVAL 6 DAY),
(11, 'CIR 동아리에서 AI 스터디를 시작합니다. 머신러닝에 관심있는 분들 환영합니다!', NOW() - INTERVAL 5 DAY);

-- 체육분과 게시글
INSERT INTO `Post` (`Club_ID`, `Content`, `post_date`) VALUES
(13, '덩키즈 주말 연습 경기 일정 안내드립니다. 토요일 오전 10시 체육관에서 뵙겠습니다!', NOW() - INTERVAL 1 DAY),
(14, '산사람 동아리 이번 주말 북한산 등반 계획입니다. 참가를 원하시는 분은 신청해주세요!', NOW() - INTERVAL 2 DAY),
(15, '산탁구 동아리 정기 연습 안내입니다. 매주 화요일, 목요일 저녁 7시에 체육관에서 만나요!', NOW() - INTERVAL 3 DAY),
(17, '위너스 동아리 배드민턴 대회 참가 안내입니다. 함께 우승을 향해 달려갑시다!', NOW() - INTERVAL 4 DAY);

-- 샘플 가입 신청
INSERT INTO `Apply` (`Student_ID`, `Club_ID`, `Self_Introduction`, `Status`) VALUES
('20240204', 1, '안녕하세요! 봉사 활동에 관심이 많아 지원하게 되었습니다. 열심히 활동하겠습니다!', '대기'),
('20240205', 2, '로타랙트의 국제 교류 활동에 참여하고 싶습니다. 잘 부탁드립니다!', '대기'),
('20240204', 7, '알고리즘 공부를 체계적으로 하고 싶어 씨부엉 동아리에 지원합니다.', '대기'),
('20240205', 14, '등산을 정말 좋아합니다. 산사람에서 함께 산을 오르고 싶습니다!', '대기'),
('20240201', 11, 'AI와 머신러닝에 큰 관심이 있습니다. CIR에서 함께 연구하고 싶습니다.', '대기'),
('20240202', 16, '서핑을 배우고 싶어서 지원하게 되었습니다. 열정적으로 참여하겠습니다!', '대기');

SELECT '✅ 샘플 데이터가 성공적으로 삽입되었습니다!' AS 'Status';
SELECT CONCAT('총 ', COUNT(*), '개의 동아리가 생성되었습니다.') AS 'Clubs' FROM `Club`;
SELECT CONCAT('총 ', COUNT(*), '명의 학생이 등록되었습니다.') AS 'Students' FROM `Student`;
SELECT CONCAT('총 ', COUNT(*), '개의 게시글이 생성되었습니다.') AS 'Posts' FROM `Post`;

