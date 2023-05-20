#!/bin/sh

# first argument is the service name, e.g. identity
# installs NET_SCH_NETEM module in kubernetes pods

for i in {1..30}
do
    echo "i = $i"
    pods=$(kubectl get pods -n alms -l app.kubernetes.io/name=$1 --field-selector status.phase=Running --no-headers | awk '{print $1}')
    for pod in $pods
    do
        kubectl exec -n alms $pod -- tc -V > /dev/null
        if [[ $? -eq 0 ]]
        then
            echo "iproute2 is already installed in pod $pod"
        else
            echo "installing iproute2 in pod $pod"
            kubectl exec -n alms $pod -- apt-get update > /dev/null 2>&1
            kubectl exec -n alms $pod -- apt-get install -y iputils-ping iproute2 > /dev/null 2>&1
            kubectl exec -n alms $pod -- tc -V
        fi
    done
    sleep 300 # 5 minutes
done
