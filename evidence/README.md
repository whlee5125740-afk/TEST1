# 실제 증거 모음
아직 사용자 PC의 실행 증거가 수집되지 않았습니다. 빈 파일이나 예상 출력은 증거가 아닙니다.

| 파일 | 기록할 내용 |
|---|---|
| 01-terminal.txt | 경로·파일 조작·권한 변경 전후 |
| 02-environment.txt | OS, Bash, Docker, Git 버전과 docker info |
| 03-docker.txt | pull, hello-world, Ubuntu, ps, logs, stats, stop |
| 04-web.txt | build, 두 포트 실행, curl 응답, 바인드 변경 전후 |
| 05-volume.txt | 볼륨 생성·연결·컨테이너 삭제 전후 cat |
| 06-git.txt | 사용자 설정, 기본 브랜치, 커밋, 원격 확인, push |
| browser-8080.png / browser-8081.png | 포트가 보이는 주소창과 화면 |
| vscode-github.png | VS Code 로그인·저장소 연동 화면(개인정보 마스킹) |

스크린샷은 위 이름으로 직접 저장합니다. 각 로그는 아래 형식으로 작성합니다.

```text
실행일시: [실제 날짜와 시간]
$ [직접 실행한 명령]
[실제 출력]
판단: [무엇을 확인했는지]
```

토큰·비밀번호·개인키·인증코드는 삭제하거나 가린 뒤 Git에 올립니다.
