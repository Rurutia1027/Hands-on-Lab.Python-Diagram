from diagrams import Diagram, Cluster
from diagrams.aws.network import CloudFront, ELB, VPC
from diagrams.aws.compute import ECS, EKS, EC2, EC2ContainerRegistry as ECR
from diagrams.aws.devtools import Codepipeline, Codebuild, Codedeploy
from diagrams.aws.database import RDSInstance, DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import IdentityAndAccessManagementIam as IAM
from diagrams.aws.general import User

with Diagram(
    "AWS SaaS: CI/CD -> Prod (simplified)",
    filename="aws_saas_pipeline",
    show=False,
    outformat=["png", "svg"],
    direction="LR"
):
    # Users & CDN
    user = User("Customer")
    cf = CloudFront("cdn")
    alb = ELB("alb")
    user >> cf >> alb

    # VPC / Production
    with Cluster("VPC / Prod"):
        with Cluster("Compute"):
            ecs = ECS("ecs-cluster")
            # eks = EKS("eks-cluster")
        db_primary = RDSInstance("user-db")
        cache = DynamodbTable("session-store")
        storage = S3("assets-bucket")

    # CI/CD pipeline
    code_repo = IAM("git-repo (SaaS)")
    pipeline = Codepipeline("CodePipeline")
    build = Codebuild("Build")
    ecr = ECR("ECR Repository")
    deploy = Codedeploy("CodeDeploy")

    code_repo >> pipeline >> build >> ecr >> deploy >> ecs
    ecs >> db_primary
    ecs >> cache
    ecs >> storage

    # Events / Analytics
    events = Eventbridge("events")
    ecs >> events