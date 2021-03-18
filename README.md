# PathComp
PathComp is a web-based competition for school age participants. Participants are asked to "Beat the Pathologists" by annotating a series of WSI. The competition includes four levels: Mild, Hot, Spicy and Supercharger of different difficulty. Each participant starts from the Mild level and has to correctly annotate at least half of the cells included in the image to proceed to the next level.

# Getting Started
First, install
- Docker [here](https://www.docker.com/get-started).
- Docker-Compose [here](https://docs.docker.com/compose/install/)

note: If you've already installed Docker Desktop/Toolbox for either Windows or Mac, you already have Docker Compose.

# Annotation Data Setup
Under the static directory there is the patch directory which includes two sub-folders. One for the competition and another one for practicing. 
## Competition: 
The competition folder includes 4 numbered sub-folders. Each number corresponds to one of the four levels available. 

i.e 1 = Mild, 2 = Hot, 3 = Spicy and 4 = Supercharger 

Each level folder has to include two sub-folders called **image** and **json**. 
The image to be annotated must be stored in the image folder while the correct answer must be stored in the json folder. Please note that both files need to have the same name.
    
## Practice
The practice folder includes only 2 sub-folders for the Mild and Hot levels. However, you can populate it with the remaining two. It follows the same structure as the competition folder.

# Annotation data for Participants
Each participant will have their own folder under the directory called annotation.

Each participant's folder will contain two sub-folders: **competition** and **history**.
- competition: Used to store the data related to the participant's ongoing work
- history: Used to keep the data submitted by the participant

Setup
---
1. Rename the .env.example file to .env.dev

2. Run the below command to generate your own secret key
```bash
python -c "import secrets; print(secrets.token_urlsafe())"
```

3. Copy the generated secret key and paste it in .env.dev

Development
---
1. Build and deploy the docker container by running

```bash
docker-compose up --build -d
```

2. If it's your first time running the container, run this command to populate the database
```bash
docker-compose exec pathcomp python manage.py migrate --noinput
```

3. The application can be accessed at
```bash
   localhost:8000
   ```
4. Stop the application by running

```bash
docker-compose down
```

5. Restart the application by running
```bash
docker-compose up -d
```
