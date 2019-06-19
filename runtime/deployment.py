from kubernetes import client

def create(betav1, name, image, ports, namespace="default"):
    deployment = _create_deployment_object(name, image, ports)
    api_response = _create_deployment(betav1, deployment, namespace)
    return deployment, api_response

def read(betav1, name, namespace="default"):
    return betav1.read_namespaced_deployment(namespace=namespace, name=name)

def delete(v1, name, namespace="default"):
    # Delete deployment
    api_response = v1.delete_namespaced_deployment(
        name=name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def update(betav1, name, deployment, namespace="default", replicas=1):
    # Update deployment replicas
    deployment.spec.replicas = replicas
    # Update the deployment
    api_response = betav1.patch_namespaced_deployment(
        name=name,
        namespace=namespace,
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))

def _create_deployment_object(name, image, ports):
    # Configureate Pod template container
    container = client.V1Container(
        name=name,
        image=image,
        ports=[client.V1ContainerPort(container_port=i) for i in ports])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"app": name}),
        template=template)
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment


def _create_deployment(betav1, deployment, namespace):
    # Create deployement
    api_response = betav1.create_namespaced_deployment(
        body=deployment,
        namespace=namespace)
    print("Deployment created. status='%s'" % str(api_response.status))
    return api_response
