#!/bin/sh

# first argument is the service name, e.g. identity
# installs NET_SCH_NETEM module in kubernetes pods

for i in {1..36}
do
    pods=$(kubectl get pods -n alms -l app.kubernetes.io/name=$1 --field-selector status.phase=Running --no-headers | awk '{print $1}')
    for pod in $pods
    do
        kubectl exec -n alms $pod -- tc -V > /dev/null
        if [[ $? -eq 0 ]]
        then
            echo "iproute2 is already installed in pod $pod"
        else
            echo "installing iproute2 in pod $pod"
            kubectl exec -n alms $pod -- apt-get update > /dev/null
            kubectl exec -n alms $pod -- apt-get install -y iproute2 > /dev/null
            kubectl exec -n alms $pod -- tc -V 
        fi
    done
    sleep 300 # 5 minutes
done
