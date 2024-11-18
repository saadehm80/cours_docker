import os
import requests
import getpass
# définition de l'adresse de l'API
api_address =os.environ.get('API_IP')
# port de l'API
api_port = os.environ.get('API_PORT')

# Parametres de connexion
username=input("Veuillez saisir le username:")
#password=input("Veuillez saisir le mot de passe:")
password=getpass.getpass ( prompt = 'Veuillez saisir le mot de passe : ' , stream = None ) 
# requête
r = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': username,
        'password': password
    }
)

output = '''
============================
    Authorization test
============================

request done at "/permissions"
| username={username}
| password={password}

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
    permissions= r.json()['permissions']
else:
    test_status = 'FAILURE'

message_output=output.format(username=username,password=password,status_code=status_code, test_status=test_status)

if status_code == 200:
	message_output+="Vous avez accès à:\n"
	for permission in permissions:
		message_output+="- "+permission+"\n"

print(message_output)
# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('my_app_logs/api_test.log', 'a') as file:
        file.write(message_output)

