# 사용자 PC 준비
아직 설치 여부가 확인되지 않았습니다. 이미 준비되어 있다면 중복 설치하지 않습니다.

1. Windows PowerShell에서 `wsl --status`, `wsl -l -v`로 Ubuntu와 버전 2를 확인합니다. 미설치라면 `wsl --install -d Ubuntu`로 설치하고 재부팅 안내에 따릅니다. 조직 PC는 관리자 정책을 확인합니다.
2. Docker Desktop 공식 안내 https://docs.docker.com/desktop/setup/install/windows-install/ 에서 설치합니다. 실행 후 WSL2 엔진과 Ubuntu 연동을 확인합니다. 설치·로그인 GUI 외 실습은 Ubuntu CLI에서 수행합니다.
3. Ubuntu에서 `docker --version`, `docker info`를 실행합니다. CLI 버전만 나오고 Server에 오류가 나면 엔진 연결이 완료되지 않은 것입니다.
4. Ubuntu에서 `git --version`, `curl --version`을 확인합니다. 없다면 `sudo apt update` 후 `sudo apt install git curl`을 실행합니다.
5. VS Code와 WSL 확장을 준비합니다. Ubuntu에서 프로젝트로 이동해 `code .`를 실행합니다. VS Code의 GitHub 로그인은 화면 안내에 따라 사용자 본인이 진행합니다.
6. Windows 경로 대신 Ubuntu 홈 아래에 폴더를 두고 진행합니다. 전역 권한 변경이나 `chmod 777`은 필요하지 않습니다.
