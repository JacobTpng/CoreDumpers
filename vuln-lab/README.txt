# vuln-lab  — Spring4Shell demo container

Builds intentionally vulnerable Tomcat 9 + Spring-Boot 2.6.4 WAR that will be exploited. 
Isolated from the rest of the repo to spin it up with single command
------------------------------------------------

## Quick-start

Must have docker installed. Can get it at https://docs.docker.com/desktop/install/windows-install/

```bash
# from repo root
docker compose up --build -d springlab
# wait 10s for Tomcat to unpack WAR
curl http://localhost:8080/
