# EKS EXTRAS 

The following EKS extras are opinionated deploys, they will work with predefined defaults described below. 

---

## Global Inputs

**Cluster Name**

The EKS cluster you wish to use with the EFS CSI Driver.


## EFS CSI Driver

Installs <a href="https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html" target="_blank">EFS CSI Controller</a> and creates an `efs-sc` kubernetes `storageClass` using the EFS file system selected.
Once deployed you will be able to deploy PVCs with an EFS back end, see below for an example:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-claim
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-sc
  resources:
    requests:
      storage: 5Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: efs-app
spec:
  containers:
    - name: app
      image: centos
      command: ["/bin/sh"]
      args: ["-c", "while true; do echo $(date -u) >> /data/out; sleep 5; done"]
      volumeMounts:
        - name: persistent-storage
          mountPath: /data
  volumes:
    - name: persistent-storage
      persistentVolumeClaim:
        claimName: efs-claim

```

--- 

## Cluster Autoscaler 

Installs <a href="https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md" target="_blank">Cluster Autoscaler</a>

--- 
## ALB Ingress Controller 
Installs <a href="https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html" target="_blank">AWS Load Balancer Controller</a>


### Prerequisites
To create internal load balancers you will need to tag at least two private subnets with the following tags:
```
kubernetes.io/role/internal-elb: 1
```

To create internet facing load balancers you will need to tag at least two private subnets with the following tags:
```
kubernetes.io/role/elb: 1
```

### Ingress Class

This install creates an ingress class named `alb` which you can use in your `Ingress manifests` to create an ingress, the example below will create an ALB with listeners on port 80/443. Note the `kubernetes.io/ingress.class` annotation is `alb`.

```

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: app1
  name: app1-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/backend-protocol: "HTTP"
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS":443}]'
    alb.ingress.kubernetes.io/actions.ssl-redirect: '{"Type": "redirect", "RedirectConfig": { "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"}}'
spec:
  rules:
    - host: test-app.kinect.internal
      http:
        paths:      
        - backend:
            service:
              name: ssl-redirect
              port:
                name: use-annotation
          path: /
          pathType: ImplementationSpecific
        - backend:
            service:
              name: app1
              port:
                number: 80
          path: /*
          pathType: ImplementationSpecific              
```

For a full list of annotations refer to <a href="https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/guide/ingress/annotations/" target="_blank">this link</a>


---
## Metrics Server
Installs <a href="https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html" target="_blank">Metrics Server</a>


---
## Fluent-Bit log shipping to Cloudwatch
Installs <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html" target="_blank">Fluent-Bit Logs to Cloudwatch</a>
Once installed container logs will ship to cloudwatch, you can set the retention policies by setting the `Log Retention in Days` input.
The logs will be stored in `/aws/eks/<cluster_name>/logs` 
