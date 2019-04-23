# SysteminfIuxdbGrafana
## running docker
   ### load image and add repository
    docker load -i influxdb.tar
    docker tag <IMAGE ID> influxdb

    docker load -i grafana.tar
    docker tag <IMAGE ID> grafana

    docker load -i system-information.tar
    docker tag <IMAGE ID> system-information

    docker run -d -p 8086:8086 -v /etc/localtime:/etc/localtime --name influx influxdb
    docker run -d -p 3000:3000 -v /etc/localtime:/etc/localtime --link influx:influx --name grafana grafana
    docker run --net=host -ti -v /etc/localtime:/etc/localtime system-information /bin/bash


    // you are now in docker container and should "cd /home/inter-test "
    nohup python3 cpu_memo_disk.py params1 > nohup.out 2>&1 & 
    // Sign out container
    curl +P+Q

## with open link http:ip:3000 and then
   * create datasourse
   * use influxdb datasourse
   * Assign url adress(not localhost) and influxdb port
   * database is sxu, user and password not need to fill in
   * save and test

## new dashboard
   * Choose Visualization and use Graph
   * you can Y-max and Y-min in Visualization and title use Genneral
   * In Queries, change Queries to datasourse what the create influxdb datasourse
   * To write sql and change Collection time in the upper right corner

## node
   ## The time displayed on the dashboard is not synchronized
    The time zone of the influxdb data is the time zone of the docker container. The default is utc. Unless you specify it with ** -v /etc/localtime:/etc/localtime ** , you should specify the same time zone as the docker container in the dashboard.       
