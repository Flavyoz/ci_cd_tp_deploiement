# Password Validator API — CI/CD Pipeline

API FastAPI qui valide la robustesse d'un mot de passe (longueur, majuscule, minuscule, chiffre, caractère spécial), déployée automatiquement sur une VM Azure à chaque push sur `main`.

## Fonctionnement du pipeline

Chaque push sur `main` déclenche un workflow GitHub Actions (`.github/workflows/ci-cd.yml`) composé de 4 jobs enchaînés :

1. **`unit-tests`** — installe les dépendances Python et exécute les tests unitaires (`pytest tests/test_unit.py`) sur la logique de validation, isolée de toute dépendance externe.
2. **`e2e-tests`** *(dépend de `unit-tests`)* — démarre le serveur `uvicorn` en arrière-plan sur le runner, attend qu'il soit prêt, puis exécute des tests E2E (`pytest tests/test_e2e.py`) qui envoient de vraies requêtes HTTP via `requests` contre les endpoints `/health` et `/validate-password`.
3. **`build-and-push`** *(dépend de `unit-tests` et `e2e-tests`)* — ne s'exécute que si les deux jobs précédents ont réussi. Construit l'image Docker, l'authentifie sur Docker Hub via un access token, et la pousse sur le registre.
4. **`deploy`** *(dépend de `build-and-push`)* — se connecte en SSH à la VM Azure (via `appleboy/ssh-action`), récupère la dernière image (`docker pull`), arrête/supprime l'ancien conteneur s'il existe, relance un nouveau conteneur avec un nom fixe, et vérifie que l'application répond via `curl /health`.

Si un job échoue, tous les jobs suivants qui en dépendent (`needs:`) sont automatiquement annulés — la pipeline s'arrête avant d'aller plus loin.

## Comment le déploiement est déclenché

Automatiquement, sans aucune action manuelle : dès qu'un commit est poussé sur la branche `main`, GitHub Actions détecte l'événement `push` et lance le workflow de bout en bout. Aucune intervention humaine n'est nécessaire entre le `git push` et l'application mise à jour sur la VM.

## Idempotence du déploiement

Le conteneur est lancé avec un nom fixe (`myapp`). À chaque déploiement, le script SSH exécute :
```bash
docker stop myapp || true
docker rm myapp || true
docker run -d --name myapp -p <port>:8000 <image>
```
Le `|| true` évite que le script échoue si aucun conteneur `myapp` n'existe encore (premier déploiement). Relancer le workflow ou repousser le même commit ne crée donc jamais de doublon : l'ancien conteneur est toujours proprement arrêté et remplacé avant qu'un nouveau ne démarre.

## Choix techniques

- **FastAPI** plutôt que Flask : validation automatique du body JSON via Pydantic, documentation interactive générée automatiquement (`/docs`), pratique pour tester les endpoints manuellement pendant le développement.
- **`/health`** : endpoint de vérification sans logique métier ni dépendance externe (pas de base de données), utilisé à la fois comme prérequis avant les tests E2E et comme vérification finale post-déploiement.
- **Secrets GitHub Actions** : aucun identifiant en clair dans le dépôt — les identifiants Docker Hub (username + access token) et les informations de connexion SSH à la VM (host, user, mot de passe) sont stockés dans `Settings > Secrets and variables > Actions`.
- **VM partagée** : la VM Azure étant mutualisée entre plusieurs projets, le nom du conteneur et le port exposé ont été choisis pour éviter tout conflit avec les déploiements des autres projets sur la même machine.

## Lancer le projet en local

```bash
pip install -r requirements.txt
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

```bash
pytest tests/test_unit.py -sv
pytest tests/test_e2e.py -sv   # nécessite que le serveur tourne déjà
```

```bash
docker build -t password-api .
docker run -d -p 8000:8000 password-api
```
