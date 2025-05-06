######################################################################
# spring4shell-capstone - vulnerable lab Dockerfile
# --------------------------------------------------------------------
# Builds a Tomcat-9 + Spring-5.3.15 container that is vulnerable to
# CVE-2022-22965/Spring4Shell.  Used only on local* networks a
#
#  Maintainer : <>  <you@example.com>
#  Created    : 2025-04-25
#  Last mod   : 2025-04-25
#
#  Usage      : docker-compose up -d vuln-lab
#  DANGER     : DO NOT expose this container to the public Internet.
######################################################################

FROM tomcat:9.0-jdk11

ARG SPRING_VERSION=5.3.15

#get vulnerable spring-core & friends
RUN mkdir -p /usr/local/tomcat/lib/vuln && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-webmvc/${SPRING_VERSION}/spring-webmvc-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/vuln/spring-webmvc.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-beans/${SPRING_VERSION}/spring-beans-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/vuln/spring-beans.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-context/${SPRING_VERSION}/spring-context-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/vuln/spring-context.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-core/${SPRING_VERSION}/spring-core-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/vuln/spring-core.jar

# ---- minimal demo app (acts as exploit target) -----------------------------
#renamed simple-app.war to app.war
COPY app.war /usr/local/tomcat/webapps/ROOT.war
# delete exploded folder if tomcat base image auto-expanded
RUN rm -rf /usr/local/tomcat/webapps/ROOT
# ---- install python3 for exploit demo ------------------------------------
# Force rebuild
RUN echo "rebuild triggered" && apt-get update && apt-get install -y python3

EXPOSE 8080
CMD ["catalina.sh", "run"]