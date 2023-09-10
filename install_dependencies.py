import subprocess
import sys
import os

# Vérifiez la plateforme pour déterminer la commande pip appropriée
if sys.platform.startswith('win'):
    # Windows
    pip_command = 'pip'
elif sys.platform.startswith('darwin'):
    # macOS
    pip_command = 'pip3'
else:
    # Linux et autres plateformes
    pip_command = 'pip3'

# Vérifiez si le fichier requirements.txt existe
if not os.path.exists('requirements.txt'):
    print("Le fichier requirements.txt n'a pas été trouvé.")
    sys.exit(1)

# Exécutez la commande pip pour installer les dépendances
try:
    subprocess.check_call([pip_command, 'install', '-r', 'requirements.txt'])
    print("Dépendances installées avec succès.")
except subprocess.CalledProcessError:
    print("Une erreur s'est produite lors de l'installation des dépendances.")
    sys.exit(1)