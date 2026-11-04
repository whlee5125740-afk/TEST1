# 중급 실습 절차서 — Ubuntu Bash 기준

명령을 한 줄씩 직접 실행합니다. `$`는 붙이지 않습니다. 각 절의 명령과 실제 출력은 지정된 로그에 복사합니다. `script`가 설치되어 있으면 절 시작 전 `script -q evidence/01-terminal.txt`와 같이 기록을 시작하고, 절 끝에 `exit`로 종료해도 됩니다. 인증 과정은 기록하지 않습니다. 로그 파일이 이미 있으면 다른 이름으로 보관한 후 진행합니다.

## 1. 현재 위치와 기본 명령 → 01-terminal.txt
프로젝트 폴더에서 시작합니다. 아래 `practice`는 이 과제에서 새로 만드는 폴더입니다. 기존 동명 폴더가 있으면 먼저 내용을 확인하고 새 이름을 사용합니다.

```bash
pwd
ls -la
mkdir -p practice/archive
cd practice
pwd
touch empty.txt
printf 'My first workroom
' > memo.txt
cat memo.txt
cp memo.txt memo-copy.txt
mv memo-copy.txt archive/renamed.txt
ls -la archive
rm archive/renamed.txt
ls -la archive
cd ..
```

현재 위치→생성→복사→이름변경과 이동→삭제 순서입니다. `rm`은 직접 만든 복사본 1개에만 사용합니다. `touch`는 없는 파일을 빈 파일로 만들며 기존 파일의 내용은 비우지 않습니다.

## 2. 파일과 폴더 권한 → 01-terminal.txt

```bash
chmod 600 practice/memo.txt
chmod 700 practice/archive
ls -l practice/memo.txt
ls -ld practice/archive
stat -c '%a %n' practice/memo.txt practice/archive
chmod 644 practice/memo.txt
chmod 755 practice/archive
ls -l practice/memo.txt
ls -ld practice/archive
stat -c '%a %n' practice/memo.txt practice/archive
```

비교 기준: 파일 600→644, 폴더 700→755입니다. 권한 변경은 직접 만든 연습 파일과 폴더에만 합니다.

## 3. 환경 확인 → 02-environment.txt

```bash
cat /etc/os-release
bash --version
git --version
docker --version
docker info
```

성공 판단: Docker 버전뿐 아니라 `docker info`의 Server 정보도 확인합니다. 사용자명·내부 주소 등 공개가 불필요한 정보는 가립니다.

## 4. Docker 기본 실습 → 03-docker.txt

```bash
docker pull hello-world
docker run --name jakkie-hello hello-world
docker logs jakkie-hello
docker pull ubuntu:24.04
docker run -d --name jakkie-ubuntu ubuntu:24.04 sleep infinity
docker exec jakkie-ubuntu bash -lc 'pwd; ls -la; echo "Inside Ubuntu"'
docker exec -it jakkie-ubuntu bash
```

위 마지막 명령으로 들어간 컨테이너 안에서 실행합니다.

```bash
echo "Interactive exec"
exit
```

호스트로 돌아와 확인합니다.

```bash
docker ps
docker attach jakkie-ubuntu
```

attach 직후에는 sleep 프로세스에 연결되어 입력 프롬프트가 없을 수 있습니다. **Ctrl+P를 누르고 이어서 Ctrl+Q**를 눌러 컨테이너를 유지한 채 빠져나옵니다. Ctrl+C로 종료하지 않습니다.

```bash
docker ps
docker images
docker ps -a
docker logs jakkie-ubuntu
docker stats --no-stream jakkie-ubuntu
docker stop jakkie-ubuntu
docker ps -a
docker start jakkie-ubuntu
```

hello-world는 안내문 출력 후 종료되는 것이 정상입니다. `sleep infinity`는 출력할 내용이 없어 logs가 비어 있어도 정상입니다. exec의 echo 출력은 터미널에 보이며 주 프로세스의 logs와는 다릅니다. exec는 실행 중인 컨테이너에서 새 명령을 실행하고, attach는 주 프로세스에 연결합니다. 이번 exec의 셸에서 exit해도 sleep은 유지됩니다. 반대로 주 프로세스로 셸을 실행한 `docker run -it --rm ubuntu:24.04 bash`에서 exit하면 그 컨테이너가 종료·삭제됩니다. 필요하면 이를 별도로 실행하고 전후 `docker ps -a`를 기록합니다.

## 5. 직접 작성한 Dockerfile 확인·빌드 → 04-web.txt

```bash
pwd
cat Dockerfile
cat site/index.html
docker build -t jakkie-workroom:1.0 .
docker images
docker run -d --name jakkie-web-8080 -p 127.0.0.1:8080:80 jakkie-workroom:1.0
curl -i http://localhost:8080
docker logs jakkie-web-8080
```

선택한 기반은 `nginx:alpine`입니다. 기본 서버는 그대로 사용하고 COPY로 나의 소개 화면을 넣었습니다. EXPOSE는 내부 사용 포트 표시입니다. `nginx:alpine` 태그는 시간이 지나면 다른 버전을 가리킬 수 있으므로 실제 사용 이미지 정보도 기록합니다.

```bash
docker image inspect nginx:alpine --format '{{json .RepoDigests}}'
docker image inspect jakkie-workroom:1.0 --format '{{.Id}}'
```

성공 기준: 빌드 종료 상태가 성공이고 curl에 HTTP 200 및 내 소개 문구가 보입니다. **아직 확인 결과는 아닙니다.** 브라우저에 `http://localhost:8080`을 입력하고 주소창 포함 화면을 `evidence/browser-8080.png`로 저장합니다.

## 6. 바인드 마운트와 두 번째 포트 → 04-web.txt
프로젝트 루트에 있는지 확인합니다. Dockerfile의 COPY로 저장한 8080 화면과 호스트 폴더를 연결한 8081 화면을 비교합니다.

```bash
pwd
docker run -d --name jakkie-bind-8081 -p 127.0.0.1:8081:80 --mount type=bind,source="$PWD/site",target=/usr/share/nginx/html,readonly jakkie-workroom:1.0
curl -i http://localhost:8080
curl -i http://localhost:8081
cp site/index.html practice/index-before.html
sed -i 's/작업실 준비 중/바인드 마운트 변경 확인/' site/index.html
cat site/index.html
curl -i http://localhost:8080
curl -i http://localhost:8081
```

성공 기준: 변경 전에는 두 화면 모두 ‘작업실 준비 중’, 변경 후에는 8080은 기존 문구, 8081은 ‘바인드 마운트 변경 확인’입니다. 이미지를 다시 빌드하지 않습니다. 브라우저 `http://localhost:8081`을 열어 새로고침하고 주소창 포함 화면을 `evidence/browser-8081.png`로 저장합니다. readonly는 컨테이너 쪽 쓰기를 막으며 호스트 편집은 가능합니다.

```bash
docker port jakkie-web-8080
docker port jakkie-bind-8081
docker inspect jakkie-bind-8081 --format '{{json .Mounts}}'
```

이 실습을 반복하려면 먼저 `cp practice/index-before.html site/index.html`로 원본을 복구합니다. 기존 컨테이너를 그대로 쓰면 run을 반복하지 않습니다. 새 컨테이너를 만들 때는 이름 충돌부터 확인합니다.

## 7. Docker 볼륨 영속성 → 05-volume.txt
아래 이름이 기존 과제 데이터와 겹치지 않는지 확인합니다. 기존 볼륨에 덮어쓰지 않도록 처음에는 `docker volume ls`로 점검합니다.

```bash
docker volume ls
docker volume create jakkie-workroom-data
docker run --name jakkie-volume-before --mount type=volume,source=jakkie-workroom-data,target=/data ubuntu:24.04 bash -lc 'echo "Jakkie volume practice" > /data/note.txt; cat /data/note.txt'
docker inspect jakkie-volume-before --format '{{json .Mounts}}'
docker rm jakkie-volume-before
docker run --name jakkie-volume-after --mount type=volume,source=jakkie-workroom-data,target=/data ubuntu:24.04 cat /data/note.txt
docker volume inspect jakkie-workroom-data
docker ps -a
```

성공 기준: 첫 컨테이너와 새 컨테이너 모두 `Jakkie volume practice`를 읽습니다. 기존 컨테이너가 삭제되고 다른 컨테이너가 같은 볼륨을 연결했다는 명령·출력을 함께 기록합니다. 볼륨을 삭제하는 명령은 검증 중 사용하지 않습니다.

## 8. Git·GitHub와 VS Code → 06-git.txt
기존 저장소에 덮어쓰지 않고 이번 과제 폴더에서 진행합니다. `.git`이 이미 있으면 init과 remote 추가를 반복하지 말고 현재 상태를 먼저 확인합니다.

```bash
git init -b main
git config user.name "Jakkie"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git config init.defaultBranch main
git config --list --local
git branch --show-current
```

이메일 자리에는 GitHub 설정에서 확인한 본인의 noreply 이메일을 입력합니다. `git config --list` 전체에는 인증 관련 값이 포함될 수 있어 기록 전 확인합니다. 토큰을 remote URL에 넣지 않습니다.

README 환경표·체크표를 수정하고 증거 파일을 저장한 뒤 진행합니다.

```bash
git status
git add README.md Dockerfile .dockerignore .gitignore site docs evidence
git diff --cached --stat
git commit -m "개발 작업실 기본 구성과 실습 기록"
```

GitHub 웹에서 비어 있는 저장소를 본인 계정으로 만들고 아래 주소를 실제 주소로 바꿉니다. 공개 또는 과제 제출 권한에 맞춰 설정하며, 초기 README 자동 생성은 선택하지 않습니다. 계정 인증과 화면 확인을 제외한 파일 작업·빌드·실행·Git 작업은 CLI로 수행합니다.

```bash
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git remote -v
git push -u origin main
git log -1 --oneline
git status
code .
```

HTTPS 인증은 사용자 PC의 자격 증명 관리자 또는 VS Code 안내를 이용합니다. 비밀번호·토큰·기기 인증코드를 로그에 복사하지 않습니다. push 후 GitHub에서 Dockerfile, README, 증거 링크가 실제 열리는지 확인합니다. VS Code에서 GitHub 계정 로그인과 저장소 연동을 확인하고 개인정보를 가린 화면을 저장합니다. 로그와 캡처를 나중에 추가했다면 다시 add·commit·push합니다.

## 9. 종료와 다음 실행

```bash
docker stop jakkie-web-8080 jakkie-bind-8081 jakkie-ubuntu
docker ps -a
```

다음에 같은 컨테이너로 실행하려면 `docker start jakkie-web-8080 jakkie-bind-8081`을 사용합니다. 실습 파일과 볼륨은 보관합니다. 전체 컨테이너·전체 볼륨 일괄 삭제 명령은 필요하지 않습니다.
