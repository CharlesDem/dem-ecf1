        ┌──────────────────┐        ┌────────────────────┐
        │     SCRAPERS     │        │  FICHIERS CLIENTS  │
        │                  │        │ (CSV / XLS / JSON) │
        └─────────┬────────┘        └─────────┬──────────┘
                  │                             │
                  └──────────────┬──────────────┘
                                 ▼
                       ┌──────────────────┐
                       │      MINIO       │
                       │ - fichiers scrap │
                       │ - client         │
                       │ - image livres   │                       
                       │ - versionnés ?   │
                       └─────────┬────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │   Traitements             │
                   │ (normalisation)           │
                   │  - anonymisation  clients │
                   │  - ajout geoloc           |
                   |  - nettoyage              │
                   └─────────────┬─────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │       SQL        │
                       │ (PostgreSQL etc) │
                       └──────────────────┘