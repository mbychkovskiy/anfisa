### helm charts for the anfisa projects

Forked fron: https://charts.bitnami.com/bitnami/zookeeper

how to use:
Install IBM tools:

https://cloud.ibm.com/kubernetes/clusters/c1irgj8d0f8n4viujejg/access?platformType=openshift&region=us-south&resourceGroup=0cb006627e35445db15f2e7cd2a54ba7

Install oc client:
https://console-openshift-console.asset-forome-dev-162fa491ef10b14d22843708d94ef0ba-0000.us-south.containers.appdomain.cloud/command-line-tools

oc.exe from the archive copy to the IBM tools bin folder. For windows is C:\Program Files\IBM\Cloud\bin .

Get token:
 https://c107-e.us-south.containers.cloud.ibm.com:31029/oauth/token/request

Try to log in:
oc login --token=< token > --server=https://c107-e.us-south.containers.cloud.ibm.com:30388

Try to deploy
```
#Clone this repo
git clone -b test https://github.com/ForomePlatform/anfisa.git
# Choose the project
oc project test
# Update helm requirements
helm dependency update
# first deploy
helm install druid -n test --debug --disable-openapi-validation .
# or upgrade if allready deployed
helm upgrade druid .
```
