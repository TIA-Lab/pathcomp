# PathComp
PathComp is a web-based competition for school ages participaants. This competition is forcused on asking the competition participants to attem to "Beat the Pathologists" by annotating a seriese of WSI. The competition is compsed of four levels: Mild, Hot, Spicy and Superchater. Participants begins from Mild level and correctly annotates at least half of the cells so that they can continue to the next level. 

# Getting Started
First, install
- Docker [here](https://www.docker.com/get-started).
- Docker-Compose [here](https://docs.docker.com/compose/install/)

# Annotation Data Setup
There are two patch image folders for competition and practice. 
## Competition: 
It has 1, 2, 3 and 4 sub-folder which maps to Mild, Hot, Spicy and Superchager level respectively. 

Each level folder must have **image** and **json** sub-folder. Any fatch image used for the competition has to be saved in **image** folder' and the ground true for each patch image has to be savved in **json** folder. 

It is important that each fatch image and ground true have to the same name. e.g.) patch1.png -> patch1.json

## Practice
At the moment, It has 1 and 2 which maps to Mild and Hot respectively. 

The structure of each level folder is the same as the Competition. 

# Setup Guide
## Database Setup
Copy .env.example to .env
Set the datasetbse values
- DB_ROOT_PASSWORD=
- DB_NAME=
- DB_USERNAME=
- DB_PASSWORD=
- DB_PORT=

Any database data is saved to **/mysql/data** folder. 

## Development Setup
Copy docker-compose.yml.example to docker-compose.yml

To run the PathComp
```docker-compose
docker-compose up -d
```

To stop the PathComp
```docker-compose
docker-compose down
```

# Annotation data for paticipants
There is **annotation** folder existed.
Each participant will have own folder in **annotation** folder based on an account.

Each participant folder havs two sub-folders: **competition** and **history**. 
- competition: keep data related to the current working on
- history: keep data done previously

