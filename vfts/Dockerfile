FROM eclipse-temurin:17.0.4_8-jdk-jammy

ARG JAR_FILE=app/build/libs/*.jar

COPY ${JAR_FILE} /app/app.jar

ENTRYPOINT [ "java", "-jar", "/app/app.jar" ]