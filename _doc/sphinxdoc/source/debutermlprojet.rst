
.. _l-debutermlprojet:

Bien démarrer un projet de machine learning
===========================================

.. index:: projet, machine learning, démarrage

Un projet de machine learning commence généralement avec un jeu de données et un problème à résoudre.
Celui-ce se décrit par trois éléments, des données (*X*), une cible (*Y*) et une fonction d'erreur
qui permette d'évaluer la distance entre la prédiction et la cible.
Une fois qu'on a cela, les premières étapes débutent avec presque toujours les mêmes questions :

.. contents::
    :local:

Etape 1 : quel est le type de problème ?
++++++++++++++++++++++++++++++++++++++++

* supervisé
    * régression : :math:`Y = f(X) + \epsilon`
    * classification : :math:`(c_1,...,c_k) = f(X)` pour un problème à :math:`k` classes
    * ranking
* non supervisé
    * clustering
    * réduction du nombre de dimension
    * système de recommandations

Il n'est pas rare qu'un projet requiert un assemblage de modèles de types différents.
La première étape consiste à imaginer un chemin entre les données initiales
et la valeur à prédire. Le problème est rarement non supervisé car on cherche le plus
souvent à reproduire un processus humain. L'aspect non supervisé intervient
sous la forme d'une étape intermédiaire.

Parmi les traitements non supervisé, on distingue ceux qu'on peut appliquer
sur de nouvelles données (ACP, k-means) et ceux où on ne peut pas
(t-SNE). Dans le second cas, c'est souvent une façon d'explorer les données mais
l'algorithme ne fera pas partie de la solution retenue.

Etape 2 : quelles sont les données ?
++++++++++++++++++++++++++++++++++++

* Est-ce une table classique ou un graphe ?
* Y a-t-il une dimension temporelle ?
* Nombre d'observations ?
* Nombre de variables (ou features) ?
* Quelles sont les variables connues, les variables à prédire ?
* Valeurs manquantes ?
* Variables catégorielles, discrètes ou continues,
  :ref:`Encoder les catégories <encoding-categorie-id>` ?
* Corrélations avec la cible à prédire ?

La plupart des algorithmes d'apprentissages utilisent des données numériques,
il faut convertir les variables catégorielles au format numérique.
Si une variable catégorielle est à choix unique et qu'elle contient :math:`C` catégories,
celle-ci sera multipliée en :math:`n` colonnes, une pour chaque modalité. Comme la somme de
ces colonnes est le vecteur colonne :math:`J=(1,...,1)`, la matrice :math:`X` modifiée sera corrélée.
Ceci peut poser problème à certains algorithmes d'apprentissage.

Etape 3 : séparation train/test
+++++++++++++++++++++++++++++++

Il faut faire attention à deux ou trois détails. Par exemple, si le problème est un de problème
de classification, il faut faire attention que toutes les classes à prédire sont bien **représentées**
dans les deux bases. C'est particulièrement important si l'une d'elles comporte peu d'exemples.
Si les données sont **temporelles**, il faut faire une séparation temporelle pour prédire
le futur avec le passé. Si les données sont **groupées**, il faut faire attention à ce que
les groupes ne soient pas tronqués sinon c'est l'assurance de faire du surapprentissage.

**Exemple :** un base de critiques de films.
S'il y a plusieurs critiques par films, il faut qu'un même film
ne soit pas présent dans les deux bases d'apprentisage et de test.
Pour ces films, il est fort probable que le modèle appris soit anormalement
performant sur la base de test.

Etape 4 : apprentissage d'un modèle
+++++++++++++++++++++++++++++++++++

On cale un ou plusieurs modèles sur les données d'apprentissage.
C'est de moins en moins sorcier :
`Machine learning automatique <http://www.xavierdupre.fr/blog/2015-12-11_nojs.html>`_.
Il faut foncer : apprendre un modèle tout de suite pour avoir une idée de la
difficulté du problème. On privilégiera les modèles linéaires et les arbres et décisions
si on souhaite obtenir un modèle interprétable. On optera pour les forêts aléaoires dans les autres cas.
Ces modèles présentent l'avantage de s'apprendre rapidement et de marcher sur tout type de données,
discrètes continues... Les forêts aléaoires sont également robustes au surapprentissage.

Etape 5 : mesure de la performance
++++++++++++++++++++++++++++++++++

On mesure la performance du modèle sur la base de test. Il existe certaines façons standard de le faire en
fonction des types de problèmes :

* classification
    * matrice de confusion
    * courbe ROC
    * précision / rappel
* régression
    * erreur de prédiction
    * graphe XY valeur à prédire / valeur prédite
* ranking
    * `DCG <http://en.wikipedia.org/wiki/Discounted_cumulative_gain>`_
    * `corrélation de rang <http://en.wikipedia.org/wiki/Rank_correlation>`_
* clustering
    * variance intra classe, inter classe
    * nombre d'arc coupés
* système de recommandation
    * corrélation de rang

Un modèle peut être considéré comme bon par un indicateur (:math:`R^2` par exemple)
et pourtant ne pas être assez bon pour l'usage qu'on doit en faire
(prédictions de séries temporelles).
Si la performance globale convient, on s'arrête souvent ici.
Dans le cas contraire, il faut retourner à l'étape 4 :

* La base d'apprentissage contient peut-être des points aberrants.
* La distribution d'un variable n'est pas homogène dans les bases d'apprentissage et des tests.
* Le modèle a besoin de plus de variables,
  combinaison non linéaires des variables existantes (polynômes, fonctions en escalier, ...),
  recoupement de la base de données avec une autre base.
* Les valeurs manquantes empêchent le modèle d'apprendre.
* Une variable continue ne l'est pas vraiment : distribution selon deux modes par exemple.
* ...

Voir également `Quelques astuces pour faire du machine learning <http://www.xavierdupre.fr/blog/2014-03-28_nojs.html>`_.

Etape 6 : ajouter des variables
+++++++++++++++++++++++++++++++

* Passer au logarithme lorsque les variables ont des valeurs extrêmes,
  cela réduit leur importance.
* Si les données sont temporelles : ajouter des agrégations sur des fenêtres glissantes
  (sur la semaine, le mois, l'année qui a précédé).
* Si les données peuvent être groupées : ajouter des moyennes, somme, nombre par groupes.
  Exemple : considérer la note moyenne d'un film pour savoir si une critique est positive
  ou négative.
* Utiliser la sortie d'autre modèle de machine learning.
* Ajouter des combinaisons de variables difficiles à apprendre pour un modèle
  comme un ratio (tout ce n'est pas linéaire)
* Chercher l'information qui pourrait aider un modèle à corriger une erreur en particulier.

Etape 7 : jouer à Hercule Poirot
++++++++++++++++++++++++++++++++

On atteint vite un plafond lorsqu'on essaye les modèles un par un.
Il faut maintenant extraire tout ce qu'on sait des données ou tout ce qu'on imagine savoir
pour améliorer la performance.

Quelques idées...

`Forest Fires Data Set <https://archive.ics.uci.edu/ml/datasets/Forest+Fires>`_

Ce jeu de données recense la surface brûlée par des feux de forêts.
On connaît la vitesse du vent, l'humidité, la témpérature de la zone où a eu lieu
l'incendie. Il faut prédire  la surface brûlée en fonction de ces paramètres.

Un grand nombre de valeurs sont nulles. Pourquoi ?

Pas évident de savoir, peut-être que les pompiers étaient tout proche,
peut-être qu'il n'y a pas eu de feu. Difficile de savoir. Il n'est pas évident de savoir si on peut
garder ces données ou en tout cas les traiter séparément avec une classification préalable.

Des incendies par temps de pluie en hiver ?

C'est probablement un orage avec de la foudre. En hiver, il y a peu de feu, les pompiers ne sont
pas sollicités trop souvent et ils auront le temps d'intervenir. Il n'est pas
forcément utile d'être aussi précis quant à la précision de la prédiction en hiver.

Et ::

    surface = a * température + b * vent + ...

Ou ::

    surface = a * température * vent + ...

Pour résumer, un feu aura des conditions favorables si la température
est élevée et si le vent est fort. Les effets s'additionnent ou ils
se combinent ? Dans le second cas, regrésser sur le logarithme des variables
ou ajouter le produit de tous les couples de variables est une piste à étudier.

`Bike Sharing Dataset Data Set <https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset>`_

On veut prévoir le nombre de vélo utilisés en fonction du temps.
La date fait partie des variables disponibles. Elle indique la saison.
On remarque également que le nombre de vélo partagés croît avec le temps,
signe d'une demande croissante. Les données cachent donc deux effets : la croissance
de la demande et l'impact de la météo sur la demande. Le plus simple,
pour avoir un modèle robuste dans le temps, est d'enlever la tendance
avant de passer à un problème de machine learning.

`Congressional Voting Records Data Set <https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records>`_

Dialogue improvisé... Il faut prédire le parti d'un sénaeur en fonction de ses votes passés.

* La prédiction repose presqu'entièrment sur un seul vote,
  on m'a dit qu'il fallait l'enlever dans ce cas mais je ne sais pas pourquoi.
* Ah... Et si on le faisait, que se passerait-il ?
* ...
* Si le taux de prédiction ne descend pas ?
* Cela veut dire sans doute que les démocrates et les républicains votent toujours un peu pareil.
* Si le taux de prédiction décroît fortement ?
* Leurs votes ne dépendent pas nécessairement de leur parti d'appartenance.
* Et maintenant, n'as-tu pas envie de savoir ?

Etape 8 : validation du modèle
++++++++++++++++++++++++++++++

On regarde sur quelques exemples bien choisis que le modèle proposent une réponse acceptable.
On applique des méthodes du type validation croisée.
