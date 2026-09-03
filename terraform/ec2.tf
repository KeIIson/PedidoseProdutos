# Busca a AMI mais recente do Amazon Linux 2023
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# Role IAM para a EC2 enviar mensagens para o SQS
resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "ec2_sqs_policy" {
  name = "${var.project_name}-ec2-sqs-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["sqs:SendMessage"]
      Resource = aws_sqs_queue.pedidos_queue.arn
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# Instância EC2
resource "aws_instance" "app_server" {
  ami                  = data.aws_ami.amazon_linux.id
  instance_type        = "t2.micro"
  subnet_id            = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
              #!/bin/bash
              sudo dnf update -y
              sudo dnf install python3-pip git -y
              pip3 install flask boto3

              mkdir /app
              cat << 'PYCODE' > /app/app.py
              ${file("${path.module}/../apps/app.py")}
              PYCODE

              export SQS_QUEUE_URL="${aws_sqs_queue.pedidos_queue.id}"
              export AWS_REGION="${var.aws_region}"

              nohup python3 /app/app.py > /app/app.log 2>&1 &
              EOF

  tags = { Name = "${var.project_name}-ec2" }
}