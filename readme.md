## README file: 

### Table of Contents

- [Requirements](#requirements)
- [Configuration](#configuration)
- [Run](#Run)
- [Troubleshooting](#troubleshooting)

### Requirements

To use this project, you will need to have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional if you want to run without docker compose)

You will also need to clone the project from the GitHub repository:
```
git clone https://github.com/username/project.git
```

### Configuration

After cloning the project, you will need to configure it by adding your API key to the `.env` file. Replace the `DEMO_KEY` with your actual API key.
### Run
if you want to run it for the first time:

```
docker-compose up
```

After the first time you can run it via:

```
docker-compose up --no-build
```
#### Run docker stand alone


```
docker run ---env-file ./.env
```

### Troubleshooting

If you encounter any issues, please make sure your API key is correct and in the proper place in the `.env` file. If you continue to have problems, feel free to contact me :).


My email: [s.m.malekabadi@gmail.com](s.m.malekabadi@gmail.com)