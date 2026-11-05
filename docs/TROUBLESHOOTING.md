# 트러블슈팅 — 실제 기록과 재현 연습 구분

아래 사례 1·2는 문제를 재현하고 해결하는 연습입니다. 문서 하단의 ‘노트북 실습에서 해결한 문제 2건’은 노트북에서 실제로 겪고 해결한 사례입니다. 재현 연습을 실행한 경우에는 실제 명령과 출력을 ‘재현 실습’으로 구분해 기록합니다.

## 사례 1. 포트가 이미 사용 중임
- 문제 제시: 두 번째 웹 컨테이너가 8080 포트로 시작되지 않는다.
- 원인 가설: 기존 웹 컨테이너가 같은 호스트 포트를 사용한다.
- 확인: `docker ps`와 `docker port jakkie-web-8080`으로 점유를 확인한다.
- 선택 재현: 정상 실행 중인 8080 웹 서버가 있을 때 아래를 실행한다.

```bash
docker run -d --name jakkie-port-check -p 127.0.0.1:8080:80 jakkie-workroom:1.0
```

- 예상: 포트 사용 관련 오류가 발생한다. 오류 메시지는 버전마다 다르므로 실제 출력을 기록한다.
- 해결: 기존 서버는 유지하고, 새 서버는 다른 포트를 사용한다. 실패한 컨테이너가 생성되었는지 먼저 확인한다.

```bash
docker ps -a --filter name=jakkie-port-check
```

실패한 연습 컨테이너가 확인되면 `docker rm jakkie-port-check`로 그 컨테이너만 정리한다. 8082가 비어 있는지 확인한 뒤:

```bash
docker run -d --name jakkie-port-check -p 127.0.0.1:8082:80 jakkie-workroom:1.0
curl -i http://localhost:8082
```

- 재확인: HTTP 200과 소개 화면을 확인한다. 끝나면 이 연습 컨테이너만 stop·rm한다.
- 실제 기록: [실행일 / 입력 명령 / 원문 출력 / 해결 후 결과를 작성]

## 사례 2. Dockerfile을 찾지 못함
- 문제 제시: 빌드 명령에서 Dockerfile을 찾지 못한다.
- 원인 가설: Dockerfile이 없는 하위 폴더에서 `.`을 빌드 경로로 지정했다.
- 재현·확인:

```bash
cd practice
pwd
ls -la
docker build -t jakkie-location-check:1.0 .
```

- 예상: Dockerfile을 찾을 수 없다는 오류. 실제 출력만 기록한다.
- 해결: Dockerfile이 있는 프로젝트 루트로 돌아간다.

```bash
cd ..
pwd
ls -l Dockerfile
docker build -t jakkie-location-check:1.0 .
```

- 재확인: 빌드 성공 메시지와 `docker images`에서 이미지가 보이는지 확인한다.
- 배운 점: `.`은 현재 폴더이므로 같은 명령도 실행 위치에 따라 결과가 다르다.
- 실제 기록: [실행일 / 입력 명령 / 원문 출력 / 해결 후 결과를 작성]

## 추가 참고: Docker 엔진에 연결되지 않음
`docker --version`은 CLI 설치만 확인한다. `docker info`에서 Server 연결이 실패하면 Docker Desktop 실행 상태, Ubuntu WSL 연동, 현재 Docker context를 확인한다. 원인 확인 없이 Docker 소켓 권한을 777로 바꾸거나 그룹 설정을 수정하지 않는다.

### 노트북 실습에서 해결한 문제 2건

#### 1. Git 작성자 정보가 없어 커밋이 중단됨

- **문제:** 실습 기록을 `git add`로 선택한 뒤 `git commit`을 실행했지만, 작성자 정보를 요구하며 저장이 중단됐다.
- **가설과 확인:** 노트북의 이 저장소에서 Git 작성자 이름과 이메일을 설정하지 않았다고 판단했다. Git이 작성자 정보를 설정하라는 메시지를 표시했다.
- **해결:** `git config user.name`과 `git config user.email`로 이 저장소의 작성자 정보를 설정했다. 이메일은 GitHub의 개인정보 보호용 주소를 사용했다.
- **재확인:** 같은 커밋 명령을 다시 실행해 `9395703`이 생성됐고, 이후 GitHub의 `main` 브랜치에 업로드했다.

#### 2. Docker attach 연결을 끊으려 하자 VS Code 파일 검색창이 열림

- **문제:** `docker attach`로 실습용 컨테이너에 연결한 뒤 `Ctrl+P`를 눌렀더니 VS Code 상단에 파일 검색창이 열렸다.
- **가설과 확인:** VS Code가 `Ctrl+P`를 터미널에 전달하기 전에 파일 검색 단축키로 처리한다고 판단했다. 다시 눌렀을 때도 같은 검색창이 열렸다.
- **해결:** 새 터미널에서 `docker stop jakkie-attach-laptop`을 실행해 연결을 종료했다. 이때 컨테이너 상태는 `Exited (137)`이었다.
- **재확인:** 같은 컨테이너를 다시 시작하고 `docker attach`로 연결한 뒤, 컨테이너 셸에서 `exit`를 실행했다. 이번에는 `docker ps -a`에서 `Exited (0)`을 확인했고, `evidence/11-attach-laptop.txt`에 실습 기록을 저장했다.

## 8080 포트 충돌 재현 결과

기존 웹서버가 8080번을 사용 중인 상태에서 같은 포트로 시험용 컨테이너를 실행해 포트 충돌을 확인했습니다.

[실행 명령과 오류 원문](../evidence/13-docker-volume-port.md)
