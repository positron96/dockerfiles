# Docker container to build netbeans java projects

Contains java8 and netbeans 8.1 (from ubuntu xenial repo).

You can run ant tasks in this container. It requires user.properties.file variable to 
point to a file with user-specific paths to JDK and libraries. This file is provided in
/build.properties, so to run ant you do:

    ant -Duser.properties.file=/build.properties jar
