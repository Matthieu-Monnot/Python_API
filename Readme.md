Matthieu MONNOT

TP 1 Python API

Les fichiers contienent :
- main : le code d'essai de l'API commenté et la réponse à la question 1
- top_10 : la réponse à la question 2
- top_3 : la réponse à la question 3
- stablecoin : la réponse à la question 4

Pour une question de limite du nombre de requêtes de l'API certaines approximations ont été faites. Notamment le choix de l'étude des 10 plus important stablecoin en terme de market cap afin de déterminer les 3 plus liquides en cryptos de cotation. En effet, il est peu probable qu'un stablecoin n'ai pas une capitalisation importante et se retrouve être l'actif le plus liquide en terme de devise de cotation par rapport à tous les autres actifs. Il est nécessaire de posséder une grande supply chain pour être convertible avec un volume important dans toutes les cryptos existantes.
Le même raisonnement a été suivi pour les 10 actifs les plus liquides.

Un contournement de ce problème aurait été de mettre un time.sleep conséquent entre chaque appel à l'API à l'intérieur d'une boucle itérative sur tous les cryptos disponibles par exemple. Ceci est relativement long...