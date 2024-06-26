This project is based on Adrift framework (https://github.com/IrishMarineInstitute/adrift).

This web application is used to generate drift forecasts for oil spills and floating objects for the Estonian sea area.

Current version of this application uses Leeway and OpenOil models. More models can be easily added, to do so please see guide below.

# pre requirements
- Windows, Linux or MacOS.
- Docker Desktop https://www.docker.com/products/docker-desktop/ to deploy the application in a Docker container.

# Build and run
Follow these steps to launch the application on your machine.

**Step 1**: Launch Docker Desktop

**Step 2**: Clone this project

```git clone https://github.com/alpari01/msi-adrift.git```

**Step 3**: Go to cloned project repository

```cd loputoo-2024```

**Step 4**: Build docker image

```docker-compose build .```

**Step 5**: Run docker image

```docker-compose up -d```

**Step 6**: 
In browser go to https://localhost:8080

# Additional configuration
## Change existing models configuration
All models configuration files are stored in _webapp_ directory and have the following naming: model_type.py.mustache.

Modify these files to tweak model behaviour according to your needs.

## Change application port
To change active port please modify the following files:

- **Dockerfile**: modify EXPOSE and CMD lines
- **docker-compose.yml**: modify _ports_ setting

## Add new simulation models
**Step 1**: Add new model in _models.json_ configuration file.

Follow json structure as shown with the existing models in this file.

Model type can be specified by separating model name with "_",

e.g. _MSI_Leeway_ model is of type _Leeway_ and _MSI_OpenOil_ is of type _OpenOil_.

See https://opendrift.github.io/choosing_a_model.html for more model types.

**Step 2**: Create model configuration file in the same directory with _models.json_ file.

Model configuration file should look like so: model_type.py.mustache

e.g. leeway.py.mustache

The application will pick up correct configuration file automatically based on model type specified in step 1.


## **NB!**
### _do not forget to rebuild the Docker image_
