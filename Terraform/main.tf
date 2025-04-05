

provider "aws" {
  region = "us-east-2"
}

resource "aws_ecr_repository" "apptitude_frontend" {
  name = "apptitude-frontend"
}

resource "aws_ecr_repository" "apptitude_backend" {
  name = "apptitude-backend"
}

resource "aws_ecs_cluster" "apptitude_cluster" {
  name = "apptitude-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRoles"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_policy_attachment" "ecs_task_execution_role_policy" {
  name       = "ecs-task-execution-policy"
  roles      = [aws_iam_role.ecs_task_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "apptitude_frontend_task" {
  family                   = "apptitude-frontend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["EC2"]
  cpu                      = "1024"
  memory                   = "3072"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      "name": "apptitude-frontend-container",
      "image": "${aws_ecr_repository.apptitude_frontend.repository_url}:latest",
      "memory": 3072,
      "cpu": 1024,
      "essential": true,
      "networkMode": "awsvpc",
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "apptitude_backend_task" {
  family                   = "apptitude-backend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["EC2"]
  cpu                      = "1024"
  memory                   = "3072"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      "name": "apptitude-backend-container",
      "image": "${aws_ecr_repository.apptitude_backend.repository_url}:latest",
      "memory": 3072,
      "cpu": 1024,
      "essential": true,
      "networkMode": "awsvpc",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "apptitude_frontend_service" {
  name            = "apptitude-frontend-service"
  cluster         = aws_ecs_cluster.apptitude_cluster.id
  task_definition = aws_ecs_task_definition.apptitude_frontend_task.arn
  desired_count   = 1
  launch_type     = "EC2"
  network_configuration {
    subnets         = ["subnet-abc123", "subnet-def456"]
    security_groups = ["sg-xyz789"]
  }
}

resource "aws_ecs_service" "apptitude_backend_service" {
  name            = "apptitude-backend-service"
  cluster         = aws_ecs_cluster.apptitude_cluster.id
  task_definition = aws_ecs_task_definition.apptitude_backend_task.arn
  desired_count   = 1
  launch_type     = "EC2"
  network_configuration {
    subnets         = ["subnet-abc123", "subnet-def456"]
    security_groups = ["sg-xyz789"]
  }
}
