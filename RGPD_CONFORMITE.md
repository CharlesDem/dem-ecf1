# RGPD_CONFORMITE

## 1. Objet du document
Ce document décrit les mesures mises en place pour assurer la conformité du projet avec le **Règlement Général sur la Protection des Données (RGPD – UE 2016/679)**.

---

## 2. Nature des données traitées

### Données collectées
- Données publiques issues du scraping (livres, citations, auteurs)
- Données partenaires fournies par les partenaires (fichiers Excel)
- Données de contact professionnelles :
  - Nom
  - Email
  - Numéro de téléphone
  - Adresse professionnelle

### Données exclues
- Aucune donnée sensible (art. 9 RGPD)
- Aucune donnée personnelle privée
- Aucune donnée concernant des mineurs

---

## 3. Finalité du traitement
Les données sont collectées et traitées uniquement pour :
- L’analyse et l’agrégation de données
- Des usages statistiques internes

Aucune réutilisation commerciale non déclarée n’est effectuée.

---

## 4. Base légale du traitement
Le traitement repose sur :
- **Intérêt légitime** (article 6.1.f RGPD)
- Données issues de sources publiques ou fournies volontairement par les partenaires

---

## 5. Mesures de protection des données

### 5.1 Pseudonymisation / chiffrement
Les données personnelles suivantes sont **hachées** avant stockage final:
- Nom du contact
- Adresse email
- Numéro de téléphone

Les données ne permettent pas d’identifier directement une personne physique.

### 5.2 Séparation des zones
- **Zone Bronze (MinIO)** : données brutes, versionnées
- **Zone Silver (PostgreSQL)** : données nettoyées et normalisées

---

## 6. Conservation des données
- Les données sont conservées uniquement pendant la durée nécessaire à leur exploitation.
- Aucune conservation illimitée sans justification métier.

---

## 7. Accès aux données
- Accès restreint aux services techniques
- Pas d’accès public direct aux stockages sensibles
- Authentification requise pour toute API exposée

---

## 8. Droits des personnes concernées
Conformément au RGPD, les personnes disposent des droits suivants :
- Droit d’accès
- Droit de rectification
- Droit à l’effacement
- Droit d’opposition

Toute demande peut être adressée au responsable du traitement.

---

## 9. Sous-traitants et hébergement
- Stockage objet : MinIO (self-hosted)
- Base de données : PostgreSQL (self-hosted)
- Aucun transfert hors UE

---

## 10. Violation de données
En cas de violation de données :
- Analyse immédiate de l’incident
- Mesures correctives appliquées
- Notification à l’autorité compétente si nécessaire (CNIL)

---

## 11. Responsable du traitement
Responsable du traitement :  
Chd Chd

Contact :  
chd@chd.chd

---

## 12. Mise à jour
Ce document est susceptible d’être mis à jour en fonction :
- De l’évolution du projet
- De nouvelles exigences réglementaires