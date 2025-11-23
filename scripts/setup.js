const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const isWindows = process.platform === 'win32';
const serverDir = path.join(__dirname, '..', 'server');
const clientDir = path.join(__dirname, '..', 'client');

/**
 * npm 설치 확인
 */
function checkNpm() {
  console.log('\n[0/6] 필수 도구 확인...');
  console.log('  npm 확인 중...');

  try {
    execSync('npm --version', { stdio: 'ignore' });
    console.log('  ✓ npm이 설치되어 있습니다.');
    return true;
  } catch (error) {
    console.error('  ❌ npm이 설치되어 있지 않습니다.');
    console.log('\n💡 설치 방법:');
    console.log('  - Node.js 공식 사이트에서 다운로드: https://nodejs.org/');
    console.log('  - 또는 패키지 매니저 사용:');
    console.log('    macOS: brew install node');
    console.log('    Ubuntu/Debian: sudo apt-get install nodejs npm');
    console.log('    Windows: Chocolatey 사용: choco install nodejs');
    return false;
  }
}

/**
 * Python 설치 확인
 */
function checkPython() {
  console.log('  Python 확인 중...');

  let pythonCmd = null;
  let pythonVersion = null;

  // python3 먼저 시도
  try {
    pythonVersion = execSync('python3 --version', { encoding: 'utf-8', stdio: 'pipe' }).trim();
    pythonCmd = 'python3';
    console.log(`  ✓ ${pythonVersion}이 설치되어 있습니다.`);
    return { cmd: pythonCmd, version: pythonVersion };
  } catch (error) {
    // python3 실패 시 python 시도
    try {
      pythonVersion = execSync('python --version', { encoding: 'utf-8', stdio: 'pipe' }).trim();
      pythonCmd = 'python';
      console.log(`  ✓ ${pythonVersion}이 설치되어 있습니다.`);
      return { cmd: pythonCmd, version: pythonVersion };
    } catch (e) {
      console.error('  ❌ Python이 설치되어 있지 않습니다.');
      console.log('\n💡 설치 방법:');
      console.log('  - Python 공식 사이트에서 다운로드: https://www.python.org/downloads/');
      console.log('  - 또는 패키지 매니저 사용:');
      console.log('    macOS: brew install python3');
      console.log('    Ubuntu/Debian: sudo apt-get install python3 python3-pip');
      console.log('    Windows: Python 공식 인스톨러 사용');
      return null;
    }
  }
}

/**
 * pip 설치 확인
 */
function checkPip(pythonInfo) {
  if (!pythonInfo) {
    return false;
  }

  console.log('  pip 확인 중...');

  // python -m pip 먼저 시도
  try {
    execSync(`${pythonInfo.cmd} -m pip --version`, { stdio: 'ignore' });
    console.log('  ✓ pip가 설치되어 있습니다.');
    return true;
  } catch (error) {
    // pip3 명령어 직접 시도
    try {
      execSync('pip3 --version', { stdio: 'ignore' });
      console.log('  ✓ pip3가 설치되어 있습니다.');
      return true;
    } catch (e1) {
      // pip 명령어 직접 시도
      try {
        execSync('pip --version', { stdio: 'ignore' });
        console.log('  ✓ pip가 설치되어 있습니다.');
        return true;
      } catch (e2) {
        console.error('  ❌ pip/pip3가 설치되어 있지 않습니다.');
        console.log('\n💡 설치 방법:');
        console.log(`  ${pythonInfo.cmd} -m ensurepip --upgrade`);
        console.log('  또는:');
        console.log('    macOS: brew install python3');
        console.log('    Ubuntu/Debian: sudo apt-get install python3-pip');
        console.log('    Windows: Python 설치 시 "Add Python to PATH" 옵션 선택');
        return false;
      }
    }
  }
}

/**
 * 사용자 입력 받기
 */
function question(rl, query) {
  return new Promise((resolve) => {
    rl.question(query, resolve);
  });
}

/**
 * 환경 변수 파일 확인 및 생성
 */
async function checkEnvFile() {
  console.log('\n[1/6] 환경 변수 설정 확인...');
  const envPath = path.join(serverDir, '.env');

  if (!fs.existsSync(envPath)) {
    console.log('⚠️  .env 파일이 없습니다. MySQL 계정 정보를 입력해주세요.\n');

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    try {
      const dbHost = await question(rl, 'MySQL 호스트 (기본값: localhost): ') || 'localhost';
      const dbUser = await question(rl, 'MySQL 사용자명 (기본값: root): ') || 'root';
      const dbPassword = await question(rl, 'MySQL 비밀번호: ');
      const dbName = await question(rl, '데이터베이스 이름 (기본값: club_db): ') || 'club_db';

      rl.close();

      if (!dbPassword) {
        console.error('❌ MySQL 비밀번호는 필수입니다.');
        process.exit(1);
      }

      const envContent = `DB_HOST=${dbHost}
DB_USER=${dbUser}
DB_PASSWORD=${dbPassword}
DB_NAME=${dbName}
JWT_SECRET_KEY=your_secret_key_change_this_in_production
JWT_EXPIRATION_HOURS=24
FLASK_ENV=development
PORT=5000
`;

      fs.writeFileSync(envPath, envContent, 'utf8');
      console.log('\n✓ .env 파일이 생성되었습니다.');
      console.log(`  DB_HOST=${dbHost}`);
      console.log(`  DB_USER=${dbUser}`);
      console.log(`  DB_NAME=${dbName}`);
      console.log('\n  프로덕션 환경에서는 JWT_SECRET_KEY를 변경하세요!');
    } catch (error) {
      rl.close();
      console.error('❌ .env 파일 생성 실패:', error.message);
      process.exit(1);
    }
  } else {
    console.log('✓ .env 파일이 있습니다.');
  }
}

/**
 * Python 가상환경 생성
 */
function setupPythonVenv(pythonInfo) {
  console.log('\n[2/6] Python 가상환경 설정...');
  const venvPath = path.join(serverDir, 'venv');

  if (!fs.existsSync(venvPath)) {
    console.log('가상환경을 생성합니다...');
    try {
      execSync(`${pythonInfo.cmd} -m venv venv`, {
        cwd: serverDir,
        stdio: 'inherit'
      });
      console.log('✓ 가상환경 생성 완료.');
    } catch (error) {
      console.error('❌ Python 가상환경 생성 실패.');
      console.error('Python이 올바르게 설치되어 있는지 확인하세요.');
      process.exit(1);
    }
  } else {
    console.log('✓ 가상환경이 이미 존재합니다.');
  }
}

/**
 * Python 의존성 설치
 */
function installPythonDeps() {
  console.log('\n[3/6] Python 패키지 설치...');
  const pythonCmd = isWindows
    ? path.join('venv', 'Scripts', 'python')
    : path.join('venv', 'bin', 'python');

  const pipCmd = isWindows
    ? path.join('venv', 'Scripts', 'pip')
    : path.join('venv', 'bin', 'pip');

  // 1. 가상환경 내 pip 직접 사용 시도
  try {
    execSync(`${pipCmd} install -q -r requirements.txt`, {
      cwd: serverDir,
      stdio: 'inherit'
    });
    console.log('✓ Python 패키지 설치 완료.');
    return;
  } catch (error) {
    // pip 실패 시 다음 방법 시도
  }

  // 2. python -m pip 시도
  try {
    execSync(`${pythonCmd} -m pip install -q -r requirements.txt`, {
      cwd: serverDir,
      stdio: 'inherit'
    });
    console.log('✓ Python 패키지 설치 완료.');
    return;
  } catch (error) {
    // python -m pip 실패 시 pip3 시도
  }

  // 3. 가상환경 내 pip3 시도
  try {
    const pip3Cmd = isWindows
      ? path.join('venv', 'Scripts', 'pip3')
      : path.join('venv', 'bin', 'pip3');
    execSync(`${pip3Cmd} install -q -r requirements.txt`, {
      cwd: serverDir,
      stdio: 'inherit'
    });
    console.log('✓ Python 패키지 설치 완료.');
    return;
  } catch (error) {
    // 모든 방법 실패
    console.error('❌ Python 패키지 설치 실패.');
    console.error('pip/pip3가 올바르게 설치되어 있는지 확인하세요.');
    console.error('가상환경을 재생성해보세요:');
    console.error('  rm -rf server/venv (또는 Windows: rmdir /s server\\venv)');
    console.error('  npm run setup');
    process.exit(1);
  }
}

/**
 * 데이터베이스 초기화
 */
function initDatabase() {
  console.log('\n[4/6] 데이터베이스 초기화...');
  const pythonCmd = isWindows
    ? path.join('venv', 'Scripts', 'python')
    : path.join('venv', 'bin', 'python');

  try {
    execSync(`${pythonCmd} init.py`, {
      cwd: serverDir,
      stdio: 'inherit'
    });
    console.log('✓ 데이터베이스 초기화 완료.');
  } catch (error) {
    console.error('❌ 데이터베이스 초기화 실패.');
    console.error('MySQL이 실행 중인지, .env 설정이 올바른지 확인하세요.');
    process.exit(1);
  }
}

/**
 * 프론트엔드 의존성 설치
 */
function installClientDeps() {
  console.log('\n[5/6] 프론트엔드 패키지 설치...');
  const nodeModulesPath = path.join(clientDir, 'node_modules');

  if (!fs.existsSync(nodeModulesPath)) {
    try {
      // npm이 설치되어 있는지 다시 확인
      execSync('npm --version', { stdio: 'ignore' });
      execSync('npm install', {
        cwd: clientDir,
        stdio: 'inherit'
      });
      console.log('✓ 프론트엔드 패키지 설치 완료.');
    } catch (error) {
      console.error('❌ 프론트엔드 패키지 설치 실패.');
      console.error('npm이 올바르게 설치되어 있는지 확인하세요.');
      process.exit(1);
    }
  } else {
    console.log('✓ 프론트엔드 패키지가 이미 설치되어 있습니다.');
  }
}

/**
 * 메인 실행 함수
 */
async function main() {
  console.log('======================================================================');
  console.log('🚀 동아리 플랫폼 자동 설정을 시작합니다...');
  console.log('======================================================================');

  // 필수 도구 확인
  if (!checkNpm()) {
    process.exit(1);
  }

  const pythonInfo = checkPython();
  if (!pythonInfo) {
    process.exit(1);
  }

  // pip 확인 (가상환경 생성 전에 시스템 pip 확인)
  // 가상환경 생성 후에는 자동으로 pip가 포함되지만, 
  // 가상환경 생성 자체가 pip를 필요로 할 수 있으므로 미리 확인
  if (!checkPip(pythonInfo)) {
    console.error('\n⚠️  pip가 없어도 가상환경 생성 시 자동으로 설치될 수 있습니다.');
    console.error('하지만 가상환경 생성이 실패할 경우 위의 설치 방법을 참고하세요.\n');
  }

  await checkEnvFile();
  setupPythonVenv(pythonInfo);
  installPythonDeps();
  initDatabase();
  installClientDeps();

  console.log('\n======================================================================');
  console.log('✅ 설정이 완료되었습니다!');
  console.log('======================================================================');
  console.log('\n이제 서버를 실행할 수 있습니다:');
  console.log('  npm start');
  console.log('\n💡 테스트 계정: admin / password123');
  console.log('');
}

main();

