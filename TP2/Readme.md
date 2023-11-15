TP 2 Python API

Les fichiers contiennent :
- main : l'implémentation directe de la requête de l'API de Binance
- async : la même implémentation en asynchrone
- threading_approach : la même implémentation en multi threading
- multiprocess : la même implémentation en multiprocessing
- websoc : le code pour établir une connexion à la websocket de binance et récupérer les ordres sur la paire BTC/USDT

Conclusion sur le temps de run des différentes approches : la méthode asynchrone est celle mettant le moins de temps pour requêter l'API de binance car elle permet de requêter tous les endpoints et d'attendre leur réponse en parallèle. Ainsi le temps maximum de calcul est diminué puisque le programme n'attend pas qu'une requête soit terminée pour passer à la suivante. La méthode threading est assez proche derrière puisqu'elle permet de réaliser pour un même programme plusieurs taches simultanément. Cependant ici, comme la complexité de calcul de l'algo est très faible cette approche manque d'intérêt et requiert très certainement un temps de run pour sa mise en place sur le programme. Enfin l'approche multiprocessing est très largement en dehors du contexte, cela est contre productif d'allouer un processeur à chaque requête d'API.  