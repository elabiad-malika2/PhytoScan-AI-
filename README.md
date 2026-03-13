# Contexte du projet

PhytoScan AI est une solution intelligente destinée à assister les **agriculteurs et techniciens agricoles** dans la détection et la gestion des maladies des plantes.

Dans l’agriculture moderne, l’identification rapide des maladies végétales est essentielle afin d’éviter les pertes de production et d’optimiser les traitements phytosanitaires. Cependant, de nombreux agriculteurs rencontrent des difficultés pour reconnaître les maladies des plantes, choisir les traitements appropriés et accéder à des informations fiables sur les solutions disponibles.

Pour répondre à ce besoin, **PhytoScan AI** propose une plateforme intelligente qui combine **vision par ordinateur et intelligence artificielle conversationnelle** afin d’aider les agriculteurs à diagnostiquer les maladies des plantes et à obtenir des recommandations précises.

La solution repose sur deux composants principaux :

- Un système de **détection de maladies basé sur la vision artificielle** permettant d’analyser une image d’une plante malade.
- Un **chatbot expert basé sur une architecture RAG (Retrieval-Augmented Generation)** permettant de fournir des conseils phytosanitaires fiables à partir d’une base de connaissances agricoles.

Cette plateforme permettra aux utilisateurs de **scanner une plante, identifier la maladie, évaluer sa gravité et obtenir des recommandations de traitement adaptées**.

---

# Mission

En tant que **Développeur IA**, ma mission consiste à concevoir, développer et déployer la plateforme **PhytoScan AI**, en mettant en place un système intelligent capable d’identifier les maladies des plantes et de fournir des conseils agronomiques pertinents aux agriculteurs.

---

# Fonctionnalités principales du système

## 1. Détection des maladies des plantes (Vision par ordinateur)

Le système doit permettre à l’utilisateur de **scanner une plante malade afin d’identifier la maladie**.

### Processus

1. L’utilisateur prend une photo de la plante malade.
2. L’image est envoyée au système.
3. Un modèle de **vision artificielle (Computer Vision)** analyse l’image.
4. Le système détecte la maladie probable.
5. Le système évalue **le niveau de gravité de la maladie**.

### Résultat affiché

- Nom de la maladie détectée
- Niveau de gravité
- Description de la maladie
- Recommandations de traitement

---

## 2. Chatbot Expert Agricole (RAG)

PhytoScan AI intègre un **chatbot intelligent** permettant aux agriculteurs de poser des questions sur les maladies des plantes et les traitements phytosanitaires.

Le chatbot repose sur une architecture **Retrieval-Augmented Generation (RAG)** permettant de combiner une base de connaissances agricoles avec un modèle de langage.

### Fonctionnement

1. L’utilisateur pose une question.
2. Le système recherche les informations pertinentes dans la base de connaissances.
3. Les documents les plus pertinents sont récupérés.
4. Le modèle LLM génère une réponse basée sur ces informations.

### Exemples de questions

- Comment traiter le mildiou de la tomate ?
- Quels sont les symptômes de l’oïdium ?
- Quel traitement utiliser pour une feuille jaunie ?

---

# Retrieval-Augmented Generation (RAG)

## Prétraitement et Chunking

Importer les documents agricoles :

- guides phytosanitaires
- manuels agronomiques
- documents PDF de référence

Les documents doivent être découpés en **chunks** afin de conserver le contexte.

Chaque chunk contient :

- le texte
- le type de culture
- la maladie associée
- les traitements recommandés

---

## Indexation et persistance des embeddings

Choisir une base de données vectorielle adaptée :

- ChromaDB
- FAISS
- Qdrant

Sélectionner un modèle d’embeddings :

- Hugging Face
- Sentence Transformers

Les embeddings sont ensuite stockés dans la base vectorielle.

---

## Retrieval (Récupération des informations)

Configurer un **retriever** permettant de rechercher les chunks pertinents selon la requête de l’utilisateur.

Techniques possibles :

- Similarité cosinus
- Query expansion
- Reranking avec Cross Encoder

---

## Génération de réponse

Définir un **prompt centralisé** pour guider la génération des réponses.

Le modèle LLM génère ensuite une réponse basée sur :

- les chunks récupérés
- le contexte de la question

Les réponses doivent être :

- précises
- cohérentes
- basées sur la base de connaissances.

---

# Génération de rapport de traitement

Le système doit permettre de **générer un rapport détaillé après l’analyse d’une plante**.

### Contenu du rapport

- image de la plante analysée
- maladie détectée
- niveau de gravité
- recommandations de traitement
- conseils de prévention

### Options

- Exporter le rapport en **PDF**
- Consulter l’**historique des analyses**

---

# Base de données

## Tables principales

### users

- id
- username
- email
- hashed_password
- role

### plant_scans

- id
- user_id
- image_path
- disease_detected
- severity
- created_at

### queries

- id
- user_id
- query
- response
- created_at

### reports

- id
- scan_id
- treatment_recommendation
- pdf_path
- created_at

---

# Back-end

**Framework :** FastAPI

### Fonctionnalités

- authentification des utilisateurs
- analyse d’image
- chatbot RAG
- génération de rapports
- gestion de l’historique

### Technologies

- Validation : **Pydantic**
- ORM : **SQLAlchemy**
- Authentification : **JWT**
- Base de données : **PostgreSQL**

### Configuration

- pydantic-settings
- fichiers `.env`

### Conteneurisation

- Docker
- Docker Compose

### Autres

- Gestion centralisée des exceptions
- Tests unitaires

---

# Front-end

Le système doit proposer une interface simple et intuitive destinée aux **agriculteurs et techniciens agricoles**.

### Technologies possibles

- Streamlit
- React

### Fonctionnalités principales

- interface pour scanner une plante
- affichage des résultats de diagnostic
- chatbot expert agricole
- tableau de bord utilisateur
- consultation de l’historique des analyses

---

# LLMOps

## MLFlow

Logger la configuration du pipeline RAG.

### Chunking

- taille des chunks
- overlap
- stratégie de segmentation

### Embedding

- modèle utilisé
- dimension des vecteurs

### Retrieval

- méthode de similarité
- nombre de chunks retournés

### LLM

- modèle utilisé
- température
- prompt template
- max tokens

Logger également :

- les réponses générées
- les contextes utilisés.

---

# Evaluation du RAG

Utiliser **DeepEval** pour mesurer la qualité des réponses du système.

### Métriques utilisées

- Answer relevance
- Faithfulness
- Precision@k
- Recall@k

---

# Pipeline CI/CD

Le projet doit intégrer un pipeline CI/CD permettant :

1. l’exécution automatique des tests
2. la construction de l’image Docker
3. la publication de l’image sur Docker Hub
4. le déploiement automatique de l’application

---

# Monitoring

Utilisation de **Prometheus** et **Grafana** pour surveiller :

## Infrastructure

- CPU
- RAM
- utilisation du container

## Application

- latence des requêtes
- nombre de requêtes
- taux d’erreurs

Configurer des **alertes automatiques** en cas de problème.