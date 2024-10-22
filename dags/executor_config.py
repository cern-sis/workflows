from kubernetes import client as k8s

kubernetes_executor_config = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="base",
                    resources=k8s.V1ResourceRequirements(
                        requests={"memory": "1500Mi"},
                        limits={"memory": "2Gi"},
                    ),
                )
            ],
        )
    ),
}
