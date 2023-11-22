TP 3 Python API
Matthieu Monnot & Guillaume Sima

Les fichiers contiennent :
- client : contient une méthode run qui correspond aux requêtes du client. Il appelle les fonctions "Request" afin de récupérer les résultats des calculs des 5 indicateurs et les print dans la console.
- server : contient des fonctions d'appels à l'API de binance et une class Task qui possède des méthodes pour calculer à partir des données de l'API binance les indicateurs présentés. Ces méthodes encapsulent ensuite les résultats dans le taskmanager du server pour qu'ils soient requêtables par le client.
- taskmanager.proto : ce fichier est le corps du service gRPC, il définit les messages qui peuvent circuler dans le protocole de communication ainsi que le "service" qui établit le lien entre les potentielles requêtes que le client peut faire et les réponses que le server va apporter à ces requêtes. 
- taskmanager_pb2 et taskm_pb2_grpc : fichiers générés à partir du .proto qui servent à monitorer les protocols d'envoie de message entre les intermédiaires de la communication. Ils permettent de définir les classes et méthodes du service gRPC ainsi qu'à gérér le contenu des messages et leur format.