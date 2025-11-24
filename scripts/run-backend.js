const path = require('path');
const { execSync } = require('child_process');

const isWindows = process.platform === 'win32';
const serverDir = path.join(__dirname, '..', 'server');

/**
 * 백엔드 서버 실행
 */
function runBackend() {
  const pythonCmd = isWindows
    ? path.join('venv', 'Scripts', 'python')
    : path.join('venv', 'bin', 'python');

  try {
    execSync(`${pythonCmd} run.py`, {
      cwd: serverDir,
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('백엔드 서버 실행 실패.');
    process.exit(1);
  }
}

runBackend();

