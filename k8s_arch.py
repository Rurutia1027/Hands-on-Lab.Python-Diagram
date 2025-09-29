# k8s_arch.py
from diagrams import Diagram, Cluster
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet, Cronjob
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.controlplane import APIServer, Scheduler

# output filename "k8s_arch.png" and do not show popup
with Diagram("K8S: Ingress → Service → Deployment (HPA)", filename="k8s_arch", show=False, outformat="png"):
    # Control plane
    api = APIServer("api-server")
    sched = Scheduler("scheduler")

    # Networking
    ingress = Ingress("your.domain.com")
    svc = Service("frontend-svc")

    # Worker nodes / cluster
    with Cluster("Worker Nodes"):
        with Cluster("frontend-deployment"):
            dp = Deployment("frontend-deploy")
            rs = ReplicaSet("frontend-rs")
            # three pods as replicas
            pods = [Pod(f"pod-{i+1}") for i in range(3)]

    # wiring
    ingress >> svc >> pods
    pods << rs << dp << HPA("hpa")
    api >> sched