# import argparse
from kubernetes import client, config
import deployment
import service

# parser = argparse.ArgumentParser()
# parser.add_argument("--k8conf", help="Path to K8's configuration file",
#                     type=str, default=None)
# args = parser.parse_args()
v1 = None
extv1beta1 = None

def init_kube():
    global v1, extv1beta1
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config("./config")

    v1 = client.CoreV1Api()
    extv1beta1 = client.ExtensionsV1beta1Api()

def create_dep(name, container_ref):
    global v1, extv1beta1
    dp_obj, dep_resp = deployment.create(extv1beta1, name, container_ref, [5000])
    srv_obj, srv_resp = service.create(v1, name, [5000])
    print("Deployment", dp_obj, dep_resp)
    print("Service", srv_obj, srv_resp)
    return name

def delete_dep(name):
    global v1, extv1beta1
    deployment.delete(extv1beta1, name)
    service.delete(v1, name)
    return name

def update_dep(name, replicas=1):
    global extv1beta1
    dp_obj = extv1beta1.read_namespaced_deployment(namespace="default", name=name) #OR we can fetch this from DB
    rr = int(dp_obj.status.ready_replicas) if dp_obj.status.ready_replicas else 0
    if rr is not replicas:
        deployment.update(extv1beta1, name, dp_obj, replicas=replicas)

def get_request_meta(name):
    global v1
    srv_resp = v1.read_namespaced_service(namespace="default", name=name)
    endpoint = srv_resp.metadata.self_link
    port = srv_resp.spec.ports[0].node_port
    host = client.Configuration().host.split(':')[1][2:]
    return host, port, endpoint
