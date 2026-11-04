# 트러블슈팅 — 실제 기록과 재현 연습 구분

현재 실제 장애는 확인하지 않았습니다. 아래 두 사례는 **예상 문제의 진단·재현 연습**입니다. 실제로 겪었다고 제출하지 않습니다. 재현했다면 실행 명령·출력을 붙이고 ‘재현 실습’이라고 표시합니다.

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
