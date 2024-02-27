---
title: "Dashboard Mistral - GAIA"
emoji: "🌱"
colorFrom: "green"
colorTo: "blue"
sdk: "docker"
tags:
  - "agriculture"
  - "ai"
  - "hackathon"
pinned: false
hf_oauth: false
---

![Arrière-plan](back.png)

Check out the final [dashboard](https://huggingface.co/spaces/Ferrxni/AgriHackteurs) on your browser and play with it.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Dashboard Mistral - GAIA

## Introduction

This project showcases a simple chatbot application built with Gradio and the Mistral AI API. The chatbot is designed to answer questions related to agriculture. Users can ask questions in French, and the chatbot, powered by the Mistral AI's `mistral` model, will provide responses.

## Features

- Simple chat interface for querying agricultural topics. (MVP 1)
- Interactive map with chatbot experience (MVP 2)

## Requirements

To run this application, you'll need:

- Python 3.6 or later.
- An API key from Mistral AI, Opencage and Agromonitoring.

## Setup

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**

  ```bash
  pip install -r requirements.txt
  ```

3. **To run locally**

  ```bash
  uvicorn app:app --host 0.0.0.0 --port 80
  ```

You can then go to [https://localhost:80](https://localhost:80) in your browser to see the result.

4. **Go to HuggingFace Space**

You can see the final public dashboard to the [Space](https://huggingface.co/spaces/Ferrxni/AgriHackteurs)


Vous pouvez ensuite accéder à l'application en allant sur [https://localhost:80](https://localhost:80) dans votre navigateur.

## Fonctionnalités

### Chatbot

Le chatbot utilise l'API Mistral AI pour répondre aux questions des utilisateurs sur l'agriculture.

### Génération d'une newsletter Mistral

L'application peut générer une newsletter Mistral contenant des informations pertinentes pour les agriculteurs.

### Données météorologiques en direct

L'application affiche des données météorologiques en direct pour aider les agriculteurs à planifier leurs activités.

### Newsletter

L'application envoie une newsletter régulière avec des informations et des conseils utiles pour les agriculteurs.

### Vidéos d'autres agriculteurs

L'application affiche des vidéos d'autres agriculteurs à proximité de notre emplacement, permettant aux utilisateurs de voir comment d'autres personnes gèrent leurs exploitations.

## Contribution

Les contributions sont les bienvenues ! Veuillez lire le fichier CONTRIBUTING.md pour plus de détails.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.