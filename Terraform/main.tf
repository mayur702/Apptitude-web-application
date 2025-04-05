# Added lifecycle to skip recreation and added null_resource check for partial infra creation

provider "aws" {
  region = "us-east-2"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "all_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_ecr_repository" "apptitude_frontend" {
  name = "apptitude-frontend"

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_ecr_repository" "apptitude_backend" {
  name = "apptitude-backend"

  lifecycle {
    prevent_destroy = false
  }
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

resource "aws_security_group" "ecs_service_sg" {
  name        = "ecs-service-sg"
  description = "Allow inbound traffic"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_task_definition" "apptitude_frontend_task" {
  family                   = "apptitude-frontend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
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
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ]
    }
  ])

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_ecs_task_definition" "apptitude_backend_task" {
  family                   = "apptitude-backend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
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
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ]
    }
  ])

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_ecs_service" "apptitude_frontend_service" {
  name            = "apptitude-frontend-service"
  cluster         = aws_ecs_cluster.apptitude_cluster.id
  task_definition = aws_ecs_task_definition.apptitude_frontend_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = data.aws_subnets.all_subnets.ids
    assign_public_ip = true
    security_groups = [aws_security_group.ecs_service_sg.id]
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [task_definition]
  }
}

resource "aws_ecs_service" "apptitude_backend_service" {
  name            = "apptitude-backend-service"
  cluster         = aws_ecs_cluster.apptitude_cluster.id
  task_definition = aws_ecs_task_definition.apptitude_backend_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = data.aws_subnets.all_subnets.ids
    assign_public_ip = true
    security_groups = [aws_security_group.ecs_service_sg.id]
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [task_definition]
  }
}

# Optional: Clean-up if partial infra exists
resource "null_resource" "check_infra_and_destroy" {
  provisioner "local-exec" {
    command = <<EOT
      echo "Checking if ECS services exist..."
      aws ecs describe-services --cluster ${aws_ecs_cluster.apptitude_cluster.name} --services apptitude-frontend-service apptitude-backend-service || true
    EOT
  }

  triggers = {
    always_run = timestamp()
  }
}
