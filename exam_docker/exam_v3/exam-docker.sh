
#suppresion des containers s'ils existent
 docker rm -f datascientest_container my_authorization_container my_authentication_container  my_content_container

#Creation d'un reseau special pour notre application
docker network create --driver bridge --subnet 192.168.0.0/16 my_app_network

#Recuperer l'image datascientest/fastapi:1.0.0
docker pull datascientest/fastapi:1.0.0


#Le build des toutes les images:
#-------------------------------
  #Creation de l'image de test Authentication:
  docker build -t authentication:1.0.0 .
	
  #Creation de l'image de test Authorization:
  docker build -t authorization:1.0.0 .
	
  #Creation de l'image de test content:
  docker build -t content:1.0.0 .

#Lancement des containers:
#-------------------------
  #Lancemnt du container de l'api de datascientest/fastapi
  docker run --rm -it --name data-api -p 8080:8080 --network=my_app_network datascientest/fastapi:1.0.0
  
  #Lancement du container de test Authentication
  docker run -it  --rm --name authentication --mount type=volume,src=my_volume_logs,dst=/my_app/my_app_logs/ -e "API_PORT=192.168.0.2" -e "API_IP=8000" --network=my_app_network -e "LOG=0"  authentication:1.0.0 
  
  #Quand la variable f'environnement n'est pas indiquée dans la commande de lancement, 
  #la valeur de LOG est egale a la valeur definie (par defaut =0) dans le Dockerfile correspondant
  docker run -it  --rm --name authorization --mount type=volume,src=my_volume_logs,dst=/my_app/my_app_logs/ -e "API_PORT=192.168.0.2" -e "API_IP=8000" --network=my_app_network  authorization:1.0.0

  #Lancement du container de test content
  docker run -it  --rm --name content --mount type=volume,src=my_volume_logs,dst=/my_app/my_app_logs/ -e "API_PORT=192.168.0.2" -e "API_IP=8000" --network=my_app_network -e "LOG=1"  content:1.0.0

#Lancement de docker-compose:
docker-compose up


#Lancement de tests:
#-------------------
docker exec -it my_authentication_container bash
docker exec -it my_authorization_container bash
docker exec -it my_content_container bash


