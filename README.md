# Example Anfisa Docker container for OpenShift.

In this example we deploy Anfisa to OpenShift environment.

Optional components (if this services already deployed):

Apache Druid

MongoDB

PostgreSQL

If this components (above) is not deployed, see ./infra/README.md

## How to deploy Anfisa to OpenShift via BuildConfig

1. Login to your OpenShift Cluster

2. Go to your project

`oc project PROJECT_NAME`

4. Clone this repo

`git clone https://bitbucket.org/artemsveshnikov/anfisa_openshift/`

5. Create Build Config in OpenShift Cluster

`oc create -f build_config.yaml`

6. Create Image Stream in OpenShift Cluster

`oc create -f images_stream.yaml`

7. Go to directory with repository and start building (in this step image will be built and pushed to internal container registry)

`oc start-build anfisa-v6`

8. Create ConfigMap

`oc create -f configmap.yaml`

9. Create Deployment

`oc create -f deploy_config.yaml`

`oc create -f deploy.yaml`

10. Create PVC

`oc create -f pvc.yaml`

11. Create ClusterIP

`oc create -f ip.yaml`

12. Create Ingress Route

`oc create -f route.yml`

## How to use

### Add dataset WS

1. Put your dataset to POD_NAME:/anfisa/a-setup/data/DATASET_NAME

2. Enter command:

`oc exec -it POD_NAME -- bash -c 'PYTHONPATH=/anfisa/anfisa/ python3 -m app.storage -c /anfisa/anfisa.json -m create -f -k ws -i /anfisa/a-setup/data/DATASET_NAME/inventory_file.cfg DATASET_VISIBLE_NAME'`

3. If not inventory file:

`oc exec -it POD_NAME -- bash -c 'PYTHONPATH=/anfisa/anfisa/ python3 -m app.storage -c /anfisa/anfisa.json -m create -f -k ws -s /anfisa/a-setup/data/DATASET_NAME/source_file.json.gz DATASET_VISIBLE_NAME'`

### Add dataset XL

1. Put your dataset to POD_NAME:/anfisa/a-setup/data/DATASET_NAME

2. Enter command:

`oc exec -it POD_NAME -- bash -c PYTHONPATH=/anfisa/anfisa/ python3 -m app.storage -c /anfisa/anfisa.json -m create -f -k xl -i /anfisa/a-setup/data/DATASET_NAME/inventory_file.cfg XL_DATASET_VISIBLE_NAME'`
