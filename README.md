---
title: "GAIA Hackathon"
emoji: "🌱"
colorFrom: "green"
colorTo: "blue"
sdk: "gradio"
python_version: "3.8"
sdk_version: "2.8.1"
suggested_hardware: "cpu-upgrade"
app_file: "app.py"
tags:
  - "agriculture"
  - "ai"
  - "hackathon"
pinned: false
hf_oauth: false
---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

Checkout the space HuggingFace to visualize the solution at https://huggingface.co/spaces/Ferrxni/Gaia_Mistral

#TO-DO - Brainstorming

** Système de carte interactive collaborative, AI-powered par Mistral **

*Features:*
- [ ] une sorte de réseau social 
- [ ] Reporting des datas avec Mistral AI + génération d'un dashboard ad hoc
- [ ] Profil utilisateur et centres d'intérêt pour mieux permettre au RAG de cibler ses comptes-rendus
- [ ] newsletter journalière / hebdomadaire
- [ ] filtrage utilisateur dans un rayon de 10, 50, 100km
- [ ] carte interactive avec display d'API qu'on a trouvées sur internet : Par exemple (mes idées, Clément)
  - windy pour aérologie,
  - webcams des champs
  - vidéos postées par des agriculteurs de ta région
  - personnalisation du fond de carte IGN (cf. api IGN) ; geopandas pour Python je crois
  - data.gouv.fr https://www.data.gouv.fr/fr/reuses/la-carte-interactive-des-types-delevages-et-des-regions-agricoles-en-france/
  
# Gaia Mistral Chat Demo

## Introduction

This project showcases a simple chatbot application built with Gradio and the Mistral AI API. The chatbot is designed to answer questions related to agriculture. Users can ask questions in French, and the chatbot, powered by the Mistral AI's `mistral` model, will provide responses.

## Features

- Simple chat interface for querying agricultural topics. (MVP 1)
- Interactive map with chatbot experience (MVP 2)

## Requirements

To run this application, you'll need:

- Python 3.6 or later.
- An API key from Mistral AI.

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

3. **Set Up Your API Key**

  ```bash
  API_KEY=your_mistral_ai_api_key_here
  ```

## Running the Application

To launch the chatbot, run the following command in the terminal from the project's root directory:

  ```bash
  python3 app.py
  ```

