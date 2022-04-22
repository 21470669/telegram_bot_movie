# Telegram Bot - Movie


## For development and testing on your own computer, please note the following steps

Since the project is dockerized, you will need to build an docker image followed by a docker container to run the project.

### Download the project to your local repo

```bash
git clone https://github.com/21470669/telegram_bot_movie.git
```

or simply download in zip format and extract it to the desired destination

### Build the docker image

```bash
docker build -t [image name] .
```

`[image name]` is your desired image name.

### Run a container based on the image built on your local computer

```bash
docker run --name [container name] -d [image name]
```

`[container name]` is your desired container name.

The project is running after the container is run.

## Run and stop the project on AWS console

You need AWS IAM user ID, login and password to enter the AWS cloud service console for the following steps.

### Run the project

1. Search and get in ECS (Elastic Container Service) in aws console
2. In clusters, select the name of cluster "ec2t1"
3. Select the tab "Tasks"
4. Select "Run new Tasks"
5. Choose Launch type EC2
6. Select "Run Task" at the bottom

### Stop the project

1. Search and get in ECS (Elastic Container Service) in aws console
2. In clusters, select the name of cluster "ec2t1"
3. Select the tab "Tasks"
4. Tick the checkbox of the running task
5. Select "Stop"
6. Press red button "Stop"

## Updating the image on aws

You will need to install AWS CLI to push the above tested docker image to AWS.
Please see the instruction below:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

<sub><sup>The following information is on the "view push command" of ECR (Elastic Container Registry).</sup></sub>
### For macOS / Linux
### Make sure that you have the latest version of the AWS CLI and Docker installed. For more information, see [Getting Started with Amazon ECR](http://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).
Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .
1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 833781484055.dkr.ecr.us-east-1.amazonaws.com
```
<sub><sup>Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.</sup></sub>

2. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:
```bash
docker build -t reportimage .
```
3. After the build completes, tag your image so you can push the image to this repository:
```bash
docker tag reportimage:latest 833781484055.dkr.ecr.us-east-1.amazonaws.com/reportimage:latest
```
4. Run the following command to push this image to your newly created AWS repository:
```bash
docker push 833781484055.dkr.ecr.us-east-1.amazonaws.com/reportimage:latest
```

### For Windows
### Make sure that you have the latest version of the AWS Tools for PowerShell and Docker installed. For more information, see [Getting Started with Amazon ECR](http://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).
Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .
1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use AWS Tools for PowerShell:
```bash
(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin 833781484055.dkr.ecr.us-east-1.amazonaws.com
```
2. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:
```bash
docker build -t reportimage .
```
3. After the build completes, tag your image so you can push the image to this repository:
```bash
docker tag reportimage:latest 833781484055.dkr.ecr.us-east-1.amazonaws.com/reportimage:latest
```
4. Run the following command to push this image to your newly created AWS repository:
```bash
docker push 833781484055.dkr.ecr.us-east-1.amazonaws.com/reportimage:latest
```

## To test the latest image pushed, just stop and run a new task
