#!/bin/sh

# first argument is the service name, e.g. identity
# installs NET_SCH_NETEM module in kubernetes pods

pods=$(kubectl get pods -n alms -l app.kubernetes.io/name=$1 --field-selector status.phase=Running --no-headers | awk '{print $1}')
for pod in $pods
do
    echo "installing iproute2 in pod $pod"
    kubectl exec -n alms $pod -- apt-get update > /dev/null
    kubectl exec -n alms $pod -- apt-get install -y apt-utils iproute2 > /dev/null
    kubectl exec -n alms $pod -- tc -V
done