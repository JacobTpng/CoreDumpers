# ######################################################################
# # spring4shell-capstone - vulnerable lab Dockerfile
# # --------------------------------------------------------------------
# # Builds a Tomcat-9 + Spring-5.3.15 container that is vulnerable to
# # CVE-2022-22965/Spring4Shell.  Used only on local* networks a
# #
# #  Maintainer : <>  <you@example.com>
# #  Created    : 2025-04-25
# #  Last mod   : 2025-04-25
# #
# #  Usage      : docker-compose up -d vuln-lab
# #  DANGER     : DO NOT expose this container to the public Internet.
# ######################################################################

# FROM tomcat:9.0-jdk11

# ARG SPRING_VERSION=5.3.17

# #get vulnerable spring-core & friends
# RUN mkdir -p /usr/local/tomcat/lib/vuln && \
#     curl -fsSL \
#       https://repo1.maven.org/maven2/org/springframework/spring-webmvc/${SPRING_VERSION}/spring-webmvc-${SPRING_VERSION}.jar \
#       -o /usr/local/tomcat/lib/vuln/spring-webmvc.jar && \
#     curl -fsSL \
#       https://repo1.maven.org/maven2/org/springframework/spring-beans/${SPRING_VERSION}/spring-beans-${SPRING_VERSION}.jar \
#       -o /usr/local/tomcat/lib/vuln/spring-beans.jar && \
#     curl -fsSL \
#       https://repo1.maven.org/maven2/org/springframework/spring-context/${SPRING_VERSION}/spring-context-${SPRING_VERSION}.jar \
#       -o /usr/local/tomcat/lib/vuln/spring-context.jar && \
#     curl -fsSL \
#       https://repo1.maven.org/maven2/org/springframework/spring-core/${SPRING_VERSION}/spring-core-${SPRING_VERSION}.jar \
#       -o /usr/local/tomcat/lib/vuln/spring-core.jar

# # ---- minimal demo app (acts as exploit target) -----------------------------
#   COPY app.war /usr/local/tomcat/webapps/ROOT.war
# # should uncomment org.apache.catalina.valves.AccessLogValve
#   RUN rm -rf /usr/local/tomcat/webapps/ROOT \
#       && sed -i 's|<!-- <Valve className="org.apache.catalina.valves.AccessLogValve"|<Valve className="org.apache.catalina.valves.AccessLogValve"|g' /usr/local/tomcat/conf/server.xml \
#       && sed -i 's|suffix=".txt" /> -->|suffix=".txt" />|g' /usr/local/tomcat/conf/server.xml
  
# # delete exploded folder if tomcat base image auto-expanded
# RUN rm -rf /usr/local/tomcat/webapps/ROOT

# EXPOSE 8080
# CMD ["catalina.sh", "run"]

FROM tomcat:9.0-jdk11
ARG SPRING_VERSION=5.3.15

# 1) Pull vulnerable Spring JARs directly into Tomcat's lib/
RUN curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-webmvc/${SPRING_VERSION}/spring-webmvc-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/spring-webmvc.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-beans/${SPRING_VERSION}/spring-beans-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/spring-beans.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-context/${SPRING_VERSION}/spring-context-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/spring-context.jar && \
    curl -fsSL \
      https://repo1.maven.org/maven2/org/springframework/spring-core/${SPRING_VERSION}/spring-core-${SPRING_VERSION}.jar \
      -o /usr/local/tomcat/lib/spring-core.jar

# 2) Deploy the WAR and remove any exploded root
COPY app.war /usr/local/tomcat/webapps/ROOT.war
RUN rm -rf /usr/local/tomcat/webapps/ROOT

# 3) Uncomment the AccessLogValve in server.xml
RUN sed -i '/AccessLogValve/ s/<!--[[:space:]]*//g' /usr/local/tomcat/conf/server.xml \
 && sed -i '/AccessLogValve/ s/-->//g'        /usr/local/tomcat/conf/server.xml

EXPOSE 8080
CMD ["catalina.sh", "run"]
