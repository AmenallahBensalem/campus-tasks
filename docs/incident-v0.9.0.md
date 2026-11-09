# Compte rendu d'incident : mise en service de v0.9.0 en staging

1. **Ce qui s'est passé** : la version v0.9.0 (image défectueuse, simulée en local car aucune image n'a été fournie) a été mise en service en staging ; le conteneur redémarrait en boucle avec l'erreur `variable DATABASE_URL manquante, arret du service`.
2. **Détection** : le contrôle de santé `wait-healthy.sh` a échoué à 14:25:24 (« staging non sain », code 1), soit une minute après la mise en service de 14:24:20 ; les journaux ont confirmé la cause.
3. **Action** : retour arrière à 14:25:36 en remettant `IMAGE_TAG=v1.0.0` puis `docker compose up -d`, sans reconstruire l'image ; le contrôle de santé a réussi à 14:25:41.
4. **Indisponibilité** : environ 1 min 21 s (de 14:24:20 à 14:25:41), dont 1 min d'attente du contrôle de santé et 12 s avant le lancement du retour arrière.
5. **Prévention** : exécuter le contrôle de santé dans le pipeline avant toute publication, déclencher le retour arrière automatiquement en cas d'échec, et vérifier que toutes les variables requises sont déclarées dans `.env.example`. Note : le port hôte a été 8081 au lieu de 8080 (port 8080 occupé sur la machine).
