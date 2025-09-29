# aws_saas_pipeline.py
from diagrams import Diagram, Cluster 
from diagrams.aws.network import CloudFront, ELB, VPC 
from diagrams.aws.compute import ECS, EKS, EC2 
from diagrams.aws.devtools import Codepipeline, Codebuild, Codedeploy 
from diagrams.onprem.container import Docker
from diagrams.aws.database import RDSInstance, DynamodbTable 
from diagrams.aws.storage import S3 
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import IdentityAndAccessManagementIam as IAM
from diagrams.aws.general import User 

with Diagram("AWS SaaS: CI/CD -> Prod (simplified)", filename="aws_saas_pipeline", show=False, outformat=["png", "svg"]):
    user = User("Customer")
    cf = CloudFront("cdn")
    alb = ELB("alb")

    user >> cf >> alb 

    with Cluster("VPC / Prod"):
        with Cluster("Compute"):
            ecs = ECS("ecs-cluster")
            # or EKS: 
            # eks = EKS("eks-cluster")
        db_primary = RDSInstance("user-db")
        cache = DynamodbTable("session-store")
        storage = S3("assets-bucket")

    # CI/CD pipeline 
    code_repo = IAM("git-repo (SaaS)")
    pipeline = Codepipeline("codepipeline")
    build = Codebuild("build")
    ecr = Docker("ECR (AWS Container Registry)")
    deploy = Codedeploy("codedeploy")

    code_repo >> pipeline >> build >> ecr >> deploy >> ecs 
    ecs >> db_primary
    ecs >> cache 
    ecs >> storage 

    # events/analytics 
    events = Eventbridge("events")
    ecs >> events 