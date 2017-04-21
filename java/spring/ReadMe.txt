$sudo service docker start
$sudo docker pull  wnameless/oracle-xe-11g
$sudo docker run -d -p 9090:8080 -p 1521:1521 -p 2022:22 wnameless/oracle-xe-11g

$ssh root@127.0.0.1 -p 2022
root@127.0.0.1's password:               <= enter "admin"
root@d953b39cc0a5:~# sqlplus 
Enter user-name:                         <= enter "system"
Enter password:                          <= enter "oracle"

SQL> create user boot identified by boot;
SQL> grant create session to boot;
SQL> gran crate table to boot;

1. mkdir libs, and copy ojdbc6.jar into libs

2. edit build.gradle , add
    compile fileTree(dir: 'libs', include: ['*.jar'])
in section dependencies

3. edit src/main/resources/application.properties, add 
    spring.datasource.driverClassName=oracle.jdbc.OracleDriver
    spring.datasource.url=jdbc\:oracle\:thin\:@localhost\:1521\:xe
    spring.datasource.username=boot
    spring.datasource.password=boot
    spring.jpa.hibernate.ddl-auto=create
    spring.jpa.show-sql=true
    spring.jackson.serialization.indent_output=true
4. $ ./gradlew bootRun
5. open url http://localhost:8080/
