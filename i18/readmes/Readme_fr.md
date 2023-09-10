#Aws-infos
Simplifiez la gestion de vos instances Amazon AWS EC2 avec cet utilitaire Python de ligne de commande. Générez des fichiers hosts.ini pour Ansible, des chaînes de connexion SSH pour chaque instance EC2 et configurez l'extension SSH de Microsoft pour VSCode. 🚀

Vous pouvez consulter ce fichier en anglais ici : [![🇬🇧]](https://github.com/Mohamed-Benguerraiche/aws-infos/blob/main/i18/readmes/Readme_fr.md)

# Un générateur de fichiers EC2 SSH

![Licence](https://img.shields.io/badge/license-GNU%20GPL%20v3-blue)

## Description

Ce script Python, **EC2 SSH File Generator**, simplifie le processus de gestion des configurations SSH pour les instances Amazon EC2. Il automatise la génération de fichiers SSH et la configuration des instances EC2, facilitant ainsi la récupération de leurs adresses IP et la connexion à celles-ci, en particulier après le redémarrage de l'instance lorsque les adresses IP sont réinitialisées.

### En ai-je besoin ?

La gestion des configurations SSH pour les instances EC2 peut s'avérer fastidieuse, en particulier lorsque les instances sont fréquemment redémarrées, ce qui entraîne une modification des adresses IP. Ce script vise à résoudre ce problème en générant automatiquement des fichiers de configuration SSH, vous permettant de vous connecter de manière transparente à vos instances EC2, qu'elles aient des PublicDnsNames, des PrivateDnsNames ou aucun des deux.

## Caractéristiques

- Génère automatiquement les fichiers de configuration SSH : `hosts.ini`, `connection_helper`, `ssh_config`.
- Gère les instances avec PublicDnsNames, PrivateDnsNames ou aucun nom.
- Enregistre l'état de la machine avec une sortie codée par couleur pour une visualisation facile.
- Prend en charge la configuration via un fichier YAML.
- Compatibilité multiplateforme (Linux, macOS, Windows).

##Installation

1. Installez les dépendances requises :

   ```bash
   python install_dependencies.py

2. Exécutez le script principal :
    ```bash
    python main.py

## Configuration

1. Vous pouvez personnaliser le comportement du script en éditant le fichier config/config.yml. Voici toutes les configurations clés que vous pouvez modifier :

    ```yaml
    key_path : spécifiez le chemin d'accès à votre clé SSH (par défaut : .ssh/aws.pem).
    region_name : définissez votre région AWS préférée (par défaut : eu-west-3).
    log_file : chemin d'accès au fichier journal (par défaut : logs/main_log.log).
    instance_status_log : chemin d'accès au fichier journal d'état de l'instance (par défaut : logs/instance_status.log).
    hosts_ini_file : Chemin d'accès au fichier hosts.ini (par défaut : files/hosts.ini).
    connection_helper_file : chemin d'accès au fichier connection_helper (par défaut : files/connection_helper).


## Licence

Ce projet est sous licence GNU General Public License v3.0 - voir le fichier LICENSE pour plus de détails.
Remerciements

    Un merci spécial à la Free Software Foundation pour son travail sur la licence publique générale GNU.
    Ce script a été créé par la méthode ($ man).

Pour plus de détails et d'instructions d'utilisation, veuillez vous référer à la documentation complète du code source.