resource "aws_ecs_cluster" "main" {
  name               = "${var.name}-cluster"
  # setting {
  #   name  = "containerInsights"
  #   value = var.enable_container_insights ? "enabled" : "disabled"
  # }
}

resource "aws_ecs_cluster_capacity_providers" "capacity_provider" {
  cluster_name = aws_ecs_cluster.main.name
  capacity_providers = ["FARGATE"]
}

resource "aws_cloudwatch_log_group" "ecs" {
  name = "/aws/ecs/${var.name}"
}

locals {
  container_environment_variables = concat(var.container_environment_variables,  [{ name = "AWS_REGION", value = var.region }])
  task_role_arn                   = var.task_role_arn != null ? var.task_role_arn : aws_iam_role.task[0].arn
  port_mappings                   = [ for port in var.open_ports : { containerPort = port } ]
}

resource "aws_ecs_task_definition" "main" {
  family                   = "${var.name}-task-def"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu_units
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = local.task_role_arn
  container_definitions = jsonencode([
    {
      name         = var.name
      image        = "${var.image_url}:${var.image_tag}"
      memory       = var.container_memory
      cpu          = var.container_cpu_units
      environment  = local.container_environment_variables
      portMappings = local.port_mappings,
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-region        = var.region
          awslogs-group         = aws_cloudwatch_log_group.ecs.name
          awslogs-stream-prefix = var.name
        }
      }
    }
  ])
}

resource "aws_ecs_service" "main" {
  name            = "${var.name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_groups
    assign_public_ip = var.assign_public_ip
  }
  tags                    = var.tags
  propagate_tags          = "SERVICE"
  enable_ecs_managed_tags = true
}
