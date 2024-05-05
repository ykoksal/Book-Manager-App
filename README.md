# Book Manager Web App

## Overview

This is a simple Book Manager Web Application that enables users to add, delete, and update book entries. It's developed using Python, HTML, and CSS, and utilizes Flask as the backend framework with Jinja2 for templating.

## Features

* Simple Book Manager Web App that enables adding, deleting and updating books. Developed with Python, HTML and CSS, based on Flask backend and Jinja2 frontend. 
- **Cloud-Based Deployment:** Utilized a CloudFormation template to deploy a VPC, Subnet, and an EC2 instance on AWS, facilitating the running of the web server.
- **Containerization:** Packaged the app with Docker through Github Actions, allowing for straightforward deployment onto an EC2 instance from Docker Hub.
- **CI/CD Pipeline:** Implemented a CI/CD pipeline using Github Actions. Each push to the Master branch triggers a build of the Docker image, which is then pushed to the EC2 server.
- **Secure Authentication** Implements JWT-based authentication to secure user access and efficiently manage authentication processes. This method maintains session integrity and enhances security by not storing sensitive information on the client side.

## Instructions to Deploy and Run This App on AWS EC2 Instance

### 1. Prepare Your GitHub Repository
   - Fork this repository or create a new one from it, as you prefer.
   - Enable GitHub Actions within your forked repository's settings.
   - Adjust additional workflow permissions as necessary, such as the usage of Secrets.


### 2. Deploy the CloudFormation Template
   - **AWS Console:**
     - Upload the `cloudformation_template.yaml` to the AWS console and start the stack deployment. Specify an SSH key name that you possess when prompted.
   - **AWS CLI:**
     - Download the `cloudformation_template.yaml` and navigate to its directory via terminal or command prompt.
     - Replace the placeholder values in the command below with your details. Adjust the CIDR blocks for the VPC and Subnet within the template if needed.
       ```
       aws cloudformation create-stack \
           --stack-name BookApp \
           --template-body file://cloudformation_template.yaml \
           --parameters \
               ParameterKey=KeyPairName,ParameterValue=<your-KeyPair> \
               ParameterKey=AmiID,ParameterValue=<your-AMI-ID> \
           --region <aws-region>
       ```

### 3. Set Up Docker Hub
   - Create a Docker Hub account if you don't already have one.

### 4. Configure GitHub Secrets
   - Navigate to the 'Secrets' section in the settings of your forked repository on GitHub.
   - Add the following secrets:
     - `EC2_HOST`: The public IP address of your EC2 instance.
     - `EC2_USER`: The username for your EC2 instance, typically 'ec2-user'.
     - `EC2_SSH_KEY`: The entire SSH key used for your EC2 instance.
     - `DOCKER_USERNAME`: Your Docker Hub username.
     - `DOCKER_PASSWORD`: Your Docker Hub password.

### 5. Trigger the GitHub Actions Workflow
   - Manually trigger the workflow from the 'Actions' section of your GitHub repository to start the deployment process.





