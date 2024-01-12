### EC2 Plus supports workloads based on EC2 instances with choice of file storage, database and data caching


### Pre-requisites

- Networking (VPC, Subnets, etc)


### Supported resources

#### EC2

- EC2 instances (1)
- Launch Configurations (1)
- User Data (1)
- Auto Scaling Groups (1)
- Security groups (2)
- Key pairs (1)
- Elastic IPs (3)
- Placement groups (?)
- Load balancers
    - ALB (1)
    - NLB (3)
- Reserved Instances (2/3)
- Dedicated Servers (?)
- Spot instances (2/3)
    - SpotIO integration?

#### Other

- CloudFront (2)
- Cert Mgr (2)

#### Storage

- EBS (1)
- FSx for Windows (2)
- EFS (2)

#### Databases

- RDS
    - MySQL (1)
    - Postgres (1)
    - MS SQL (1 or 2)
- Aurora
    - MySQL (1)
    - Postgres (1)

#### Other

- Tagging
- Backups
- Enable CLoudWatch
    - New Relic
- IAM (roles, policies)
    - Allow adding existing policy to EC2 role



