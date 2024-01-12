resource "aws_iam_role" "task" {
  count = var.task_role_arn == null ? 1 : 0
  name  = "${var.name}-task-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

/*resource "aws_iam_role_policy" "ecs_task_policy" {
  count  = var.task_role_arn == null ? 1 : 0
  name   = "${var.name}-policy"
  role   = aws_iam_role.task[0].id
  policy = ""
}*/

resource "aws_iam_role" "task_execution" {
  name = "${var.name}-task-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

data "aws_iam_policy" "aws_managed_task_execution_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "execution_role_policy_attachment" {
  role       = aws_iam_role.task_execution.name
  policy_arn = data.aws_iam_policy.aws_managed_task_execution_policy.arn
}