FROM amazoncorretto:17

ARG JAR_FILE=app/build/libs/*.jar

COPY ${JAR_FILE} /var/lib/app.jar

ENTRYPOINT [ "java", "-jar", "/var/lib/app.jar" ]