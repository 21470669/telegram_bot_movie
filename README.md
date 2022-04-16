# COMP7940_Project

## For development and testing on your own computer, please note the following steps

Since the project is dockerized, you will need to build an docker image followed by a docker container to run the project.

### Download the project to your local repo

```bash
git clone https://github.com/marcato-cheung-hkbu-daai/COMP7940_Project.git
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
