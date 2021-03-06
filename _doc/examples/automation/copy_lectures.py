# -*- coding: utf-8 -*-
"""
Copy documentation
==================

Copy all the documentation into one single folder
in order to serve it through a server.
"""

#########################################
# import

import sys
import os

############################
# paramètres
# root est là où sont compilés les packages
# dest est le répertoire destination
root = os.path.normpath(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..")))
dest = os.path.normpath(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "..", "documentation")))

#########################################
# Cette section ajoute des chemins pour des modules que je développe
# et que je n'installe jamais. Je pourrais me servir d'un environnement
# virtuel mais en pratique, c'est toujours un peu compliqué
# de mettre le mettre à jour en permanence.

this = os.path.abspath(os.path.dirname(__file__))
if "ensae_teaching_cs" in this:
    this = this.split("ensae_teaching_cs")[0].rstrip("\\/")
for module in ["jyquickhelper", "pyquickhelper"]:
    try:
        exec("import %s" % module)
    except ImportError:
        p = os.path.join(this, module, "src")
        print("add path", p)
        sys.path.append(p)
        exec("import %s" % module)

#########################################
# logging

from pyquickhelper.loghelper import fLOG  # publish_lectures
fLOG(OutputPrint=True)

#########################################
# import des fonctions dont on a besoin
from pyquickhelper.filehelper import synchronize_folder, explore_folder_iterfile

########################################
# récupération des répertoires compilés via un serveur jenkins
fLOG("Digging into ", root)

sub = os.path.join("_doc", "sphinxdoc", "build", "html", "index.html")
index = []
pattern = "^index.html$"
done = {}
for name in explore_folder_iterfile(root, pattern):
    if name.endswith(sub):
        pack = name[:len(name) - len(sub) - 1]
        parent, spl = os.path.split(pack)
        if "_UT_" in spl:
            parent, spl = os.path.split(parent)
        if "_UT_" in spl:
            raise ValueError("Something is weird with: '{0}'".format(name))
        index.append((spl, os.path.dirname(name)))
        if spl in done:
            raise ValueError("Duplicated package '{0}'.\n{1}".format(
                spl, "\n".join("{0}={1}".format(k, v) for k, v in sorted(done.items()))))

fLOG("Found {0} directories".format(len(index)))
for ind in index:
    fLOG("  ", ind)

########################################
# copies
for pack, folder in index:
    fLOG("########################")
    fLOG("Copy of", pack)
    fLOG("########################")
    to = os.path.join(dest, pack)
    fLOG("destination", to)
    if not os.path.exists(to):
        os.makedirs(to)
    status_file = os.path.join(dest, pack + ".txt")
    synchronize_folder(folder, to, log1=True, copy_1to2=True,
                       file_date=status_file)
