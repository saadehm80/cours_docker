import os
import requests
import getpass


#Fonction utile pour obtenir un affichage joli
def affichage_joli(chaine,taille):
	if len(chaine)>taille :
		print("Vous devez aggrandir la valeur de la variable taille")
	for  n in range(taille-len(chaine)):
		chaine=chaine+" "
	return chaine

# définition de l'adresse de l'API
api_address =os.environ.get('API_IP')
# port de l'API
api_port = os.environ.get('API_PORT')

# Parametres de connexion
username=input("Veuillez saisir le username:")
#password=input("Veuillez saisir le mot de passe:")
password=getpass.getpass ( prompt = 'Veuillez saisir le mot de passe : ' , stream = None ) 


# La methode sentiment
def sentiment(permission,phrase):
    req= requests.get(
    url='http://{address}:{port}/{permission}/sentiment'.format(address=api_address, port=api_port,permission=permission),
	    params= {'username': username,'password': password,'sentence':phrase} )
    print(req.json())
    return  req.json()['score']

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
    Content test
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
else:
    test_status = 'FAILURE'

output=output.format(username=username,password=password,status_code=status_code, test_status=test_status)


if status_code == 200:
    permissions= r.json()['permissions']
    phrases=['life is beautiful','that sucks']
    output+="\nVous avez accès à:\n"
    for permission in permissions:
        output=output+"- "+permission
        output+="\n"
    output+="-------------------------------------------------------\n"
    output+="|\t  Phrase\t\t Version    Score     |\n"
    output+="-------------------------------------------------------\n"
    for phrase in phrases:
        for permission in permissions:
            output+="|"+affichage_joli(phrase,35)+permission+"\t{:10.4}".format(sentiment(permission,phrase))+"    |\n"
            output+="-------------------------------------------------------\n"

print(output)
# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('my_app_logs/api_test.log', 'a') as file:
        file.write(output)

