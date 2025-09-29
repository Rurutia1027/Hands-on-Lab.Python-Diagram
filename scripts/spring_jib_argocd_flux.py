from diagrams import Diagram, Cluster
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.custom import Custom
from diagrams.k8s.compute import Deployment, Pod, Cronjob
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.clusterconfig import HPA

with Diagram(
    "Spring CI/CD with JIB, ArgoCD & FluxCD",
    filename="spring_jib_argocd_flux",
    show=False,
    outformat="png",
    direction="LR"   
):
    # === Source & CI/CD ===
    with Cluster("CI/CD"):
        dev = Github("Source Repo (Spring App)")
        ci = Jenkins("CI/CD Pipeline")
        jib = Docker("Jib Build")
        hub = Docker("DockerHub")
        dev >> ci >> jib >> hub

    # === GitOps controllers ===
    argocd = Custom("", "./icons/argo-cd.png")
    fluxcd = Custom("", "./icons/flux-cd.png")
    hub >> [argocd, fluxcd]

    # === Kubernetes Cluster ===
    with Cluster("Kubernetes Cluster"):
        ingress = Ingress("api.company.com")
        svc = Service("spring-service")

        with Cluster("Deployments"):
            deploy = Deployment("spring-deployment")
            with Cluster("Pods"):
                pods = [Pod(f"pod-{i+1}") for i in range(2)]
            hpa = HPA("autoscaler")
            cron = Cronjob("nightly-cron")

        argocd >> deploy
        fluxcd >> deploy

        ingress >> svc >> pods
        deploy >> pods
        deploy >> hpa
        cron >> deploy