# Docker 볼륨 정보와 8080 포트 충돌 재현

```text
$ docker volume inspect jakkie-laptop-data
[
    {
        "CreatedAt": "2026-11-05T04:06:53Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/jakkie-laptop-data/_data",
        "Name": "jakkie-laptop-data",
        "Options": null,
        "Scope": "local"
    }
]

$ docker port jakkie-web-8080 80/tcp
127.0.0.1:8080

$ docker run --rm -p 127.0.0.1:8080:80 jakkie-workroom:1.0 sh -c "exit 0"
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint busy_elion (d9127df50d9bbdd6fc1091e10ba7d39e8f54c0c7dcb681ee99e491ff1082454e): Bind for 127.0.0.1:8080 failed: port is already allocated

Run 'docker run --help' for more information
종료 코드 125
```
