#!/bin/bash

host=http://127.0.0.1:5000

nav=$host"/v1/coverage/default/"

echo nav

nb_req=20

logfile="/tmp/bob"

echo "c'est partiiiiii" > $logfile

for col in "lines" "routes" "stop_points" "stop_areas" "vehicle_journeys" "datasets" "networks" "physical_modes" ;do
    echo "******** benching $col **********" >> $logfile
    echo "*" >> $logfile
    echo "*" >> $logfile

    ab -n $nb_req -c 1 $nav$col"?depth=1" >> $logfile
done

ab -n $nb_req $nav"places?q=com" >> $logfile
ab -n $nb_req $nav"stop_areas/stop_area:SNC:SA:SAOCE87213512/stop_schedules" >> $logfile


