# button_project

This is a simple application to get an understanding of Docker Containers.
This project also includes concepts of Docker Volumes and Docker Networking

`Frontend - node.js`
`Backend - python`
`DB - mysql`

We have `three containers` in this application - Frontend, Backend and Database

Here all we do is display a webpage with `two buttons` as below :    
*INSERT SCREENSHOT*

We connect the application to a mysql database, which is a running container.
  - `Increment Counter` button increments the counter by 1 (initialized in the DB by 0)
  - `Get Counter` button retrieves the present counter value from the DB

My goal is to containerize this application and make use of most of the important Docker concepts

NOTE - build context for frontend and backend are their directories respectively

Frontend Docker Image - (Inside frontend directory)  
```
docker build -t frontend_button:1.0.0 . 
```

Backend Docker Image - (Inside backend directory)  
```
docker build -t backend_button:1.0.0 . 
```

Now that we have our images ready, lets dive into building our containers - 
But before that its necessary to have our own network specific to our project

```
docker network create button_network 
```

Also, everytime I change my source code, in this present scenario, I'll have to re-build the images so that my changes are reflected. To avoid re-building of my images, I just need to create a `Bind Mount' - which mounts my source code to the working directory of the Application, which makes both of them in sync.

### Frontend Container

```
docker run -d --name frontend \
                --volume ~/docker/button_project/frontend:/app \
                --network button_network
                -p 3000:3000
                --env-file env.vars.list 
                frontend_button:1.0.0
```


### Backend Container

Note - There's a file `env.vars.list` which consists of environment variables that are supposed to be set inside the running container. 

We can skip this by using -e flag in the docker run command like this - 

``` 
docker run -d 
    --name backend \
    --volume ~/docker/button_project/backend:/app
    --network button_network
    -e DB_PASSWORD=bd
    -p 8000:8000
    backend_button:1.0.0
```

Other Environment vars which include `DB_HOST`, `DB_USER`, `DB_NAME` are present in the backend source code (app.py). To avoid hardcoded passwords in the source code, we can pass the password using -e flag in the cli during runtime.

But to even further prevent hardcoded passwords in the cli too, we can pass `--env-file`.

``` 
docker run -d 
    --name backend \
    --volume ~/docker/button_project/backend:/app
    --network button_network
    --env-file env.vars.list
    -p 8000:8000
    backend_button:1.0.0
```

### Database Container

We need to create docker volume first to backup data present in the mysql DB.
The path to backup is `/var/lib/mysql'

``` docker volume create mysql_db ```

```
docker run -d 
          --name mysql
          --mount type=volume,src=mysql_db,dst=/var/lib/mysql
          --network button_network
          --env-file env.vars.list
          -p 3306:3306
          mysql:8.0
```

Login into the DB container - 
``` mysql -u root -p ```

Enter the password and create the Database and Table -

```sql
  CREATE DATABASE counter_db
  USE counter_db
  CREATE TABLE counter (id INT PRIMARY KEY, count INT);
  INSERT INTO counter (id, count) VALUES (1, 0);
  SELECT * FROM counter
```

Once done, all the containers are up and ready.  
Hit the URL -  
```http://localhost:3000```
and the website is ready to use !

There are multi-staged dockerfiles as well which reduce the size of the images.

### Backend Multistaged Dockerfile - 
- Here I used --prefix (which installs packages into a known isolated location, outside the default /usr/local)
Hence pip installs everything in `/install` directory - `/install/lib/python3.x/site-packages/`

- Now the COPY command copies only /install directory to the final image's /usr/local and excludes build tools, pip, setuptools etc which are not required in the final image

### Frontend Multistaged Dockerfile -  
- Here I copied package.json initially instead of copying the entire code, because
  - Docker builds images in layers and caches each layer. If there's no change in a layer, Docker reuses the previous result instead of re-running it.
  - If my code were -
  
    ```
    COPY . .
    RUN npm install
    ```
    Any change in ANY of the source code files, would make docker re-run npm install, which is not efficient.
    So to avoid re-installing a lot of npm packages we copied packages.json first

- `npm install` command creates /node_modules directory in the current working directory which is `/app`. So I copied /app of builder image to the /app directory of final image