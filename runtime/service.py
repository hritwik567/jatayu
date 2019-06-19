from kubernetes import client

def create(v1, name, ports, namespace="default"):
    service = _create_service_object(name, ports)
    api_resp = _create_service(v1, service, namespace)
    return service, api_resp

def read(v1, name, namespace="default"):
    return v1.read_namespaced_service(namespace=namespace, name=name)

def delete(v1, name, namespace="default"):
    # Delete deployment
    api_response = v1.delete_namespaced_service(
        name=name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Service deleted. status='%s'" % str(api_response.status))

def _create_service(v1, service, namespace):
    # Create deployement
    api_response = v1.create_namespaced_service(
        body=service,
        namespace=namespace)
    print("Service created. status='%s'" % str(api_response.status))
    return api_response

def _create_service_object(name, ports):
    # Creating spec
    spec = client.V1ServiceSpec(
        ports=[client.V1ServicePort(port=i) for i in ports],
        selector={"app": name},
        type="NodePort")

    # Creating Port object
    service = client.V1Service(spec=spec,
        metadata=client.V1ObjectMeta(name=name))  # V1Serice

    return service
