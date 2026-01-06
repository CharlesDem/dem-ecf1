## Projet ECF1

Ce programme a pour but de scraper des données de livres et citations sur les sites "https://quotes.toscrape.com" et "https://books.toscrape.com".
Ces données sont stockées en brut dans une instance minio dockerisée, puis nettoyée et stockées dans une base de données postgres également dockerisée. 
Ces données peuvent être interrogées via l'interface PG admin dockerisée. (voir le fichier analyse.sql)

###
Prérequis
- python 3+ et venv
- docker
- connaissances docker et SQL
- un ide type VsCode


### Mise en place du projet

- en cli docker à la racine du projet.
 
 ```
 docker compose up -d
 ```

 Une fois les composants (minio, postgres, pgadmin lancés), après quelques secondes (le temps que la base de données et les tables se créent) :
 - créer le bucket "client" dans minio et y insérer le fichier excel client "partenaire_librairies.xlsx"
 - créer un environnement virtuel venv et activez le : 
 ```
 python -m venv .venv
 .venv/scripts/activate
 ```
 - installer les dépendances :
 ```
pip install -r requirements.txt
 
 ```
-lancer le programme (en cli depuis la raicne du projet) :
```
python pipeline.py
```

Notez que les données peuvent être récupérées séparément :
- le scraping des livres
```
python book_pipeline.py
```

- le scraping des citations
```
python quote_pipeline.py

```

- la récupération du fichier client :
```
python partner_pipeline.py
```

### Requêtes SQL

Le contenu du fichier analyses.sql peut désormais être joué dans l'interface de pgadmin dockersié.
