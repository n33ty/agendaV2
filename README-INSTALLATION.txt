INSTALLATION — SYNCHRONISATION DE L'HORAIRE UCLouvain

Le dépôt GitHub doit contenir ces éléments à la racine :
- index.html (ce fichier remplace l'ancien)
- .github/workflows/sync-horaire.yml
- scripts/parse_calendar.py

Le workflow génère automatiquement data/cours.json. Le dossier data peut donc être créé automatiquement lors de la première exécution.

À faire sur GitHub :
1. Remplacer index.html par celui du paquet.
2. Vérifier/mettre à jour .github/workflows/sync-horaire.yml avec la version de ce paquet.
3. Vérifier/mettre à jour scripts/parse_calendar.py avec la version de ce paquet.
4. Dans Settings > Secrets and variables > Actions, conserver le secret UCL_CALENDAR_URL (ne pas publier sa valeur).
5. Dans Actions, lancer « Synchroniser horaire UCLouvain » avec Run workflow.
6. Vérifier que data/cours.json est créé ou mis à jour, puis actualiser le site avec Ctrl+F5.

RÈGLE DES SEMAINES : les cours UCLouvain sont importés à partir de la semaine ISO 3 comprise. Les semaines ISO 1 et 2 gardent leur planning local. À partir de la semaine ISO 3, les cours locaux existants sont remplacés par les cours du calendrier, sans supprimer les blocs personnels d'étude, sport ou Uber Eats.

Les heures sont converties en heure de Bruxelles et les locaux apparaissent dans les blocs de cours et dans leur fiche détaillée.

IMPORTANT : ne pas remplacer index.html si tu as fait des changements récents non inclus dans ce paquet. Dans ce cas, il faut fusionner les modifications plutôt que remplacer le fichier entier.
