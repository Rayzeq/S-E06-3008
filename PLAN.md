# Plan d'écriture de tests

## Tests unitaires

### Tests de désérialisation d'un `PointSet`

Si le services `PointSet` est mal implémenté est renvoie des données au mauvais format, ou que la transmission réseau est corrompue, la désérialisation d'un `PointSet` peut échouer. On teste si celle-ci est implémentée correctement.

- Entrée: vide
  Résultat: exception

- Entrée: 3 octets quelconques
  Résultat: exception

- Entrée: `b"\x00\x00\x00\x00"`
  Résultat: `[]`

- Entrée: `b"\x01\x00\x00\x00"`
  Résultat: exception (nombre de annoncés != nombre de points réels)

- Entrée: `b"\x00\x00\x00\x00\x00"`
  Résultat: exception (données superflues)

- Entrée: `b"\x01\x00\x00\x00\x3f\x80\x00\x00"`
  Résultat: exception (coordonnée Y manquante)

- Entrée: `b"\x01\x00\x00\x00\x3f\x80\x00\x00\xbf\x80"`
  Résultat: exception (2 octets manquante)

- Entrée: `b"\x01\x00\x00\x00\x3f\x80\x00\x00\xbf\x80\x00\x00"`
  Résultat: `[Point(1, -1)]`

- Entrée: petite liste de 5 points dans le bon format
  Résultat: la liste Python

### Tests de sérialization d'un `Triangles`

Sérialisation du `PointSet` contenu dans le `Triangles`: non nécéssaire, si le `PointSet` retourné par le `PointSetManager` est au bon format, sa re-sérialisation n'est pas nécéssaire.
Le `PointSet` sera donc omis des exemples de résultats suivants (mais il sera nécéssaire dans les vrais tests en Python).

- Entrée: 0 triangles
  Résultat: `b"\x00\x00\x00\x00"`

- Entrée: 1 triangle (0 -> 1 -> 2)
  Résultat: `b"\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"`

- Entrée: 5 triangles
  Résultat: les triangles représentés dans le bon format

### Tests de l'algorithme de triangulation

- Entrée: 0 points
  Résultat: erreur

- Entrée: 1 point
  Résultat: erreur

- Entrée: 2 points
  Résultat: erreur

- Entrée: 3 points
  Résultat: un triangle contenant les 3 points

- Entrée: 4 points
  Résultat: 2 triangles, avec 2 points qui n'apparaissent qu'une seule fois, et 2 points qui apparaissent 2 fois

- Entrée: points confondus (3 ou plus)
  Résultat: à determiner, une erreur ou un triangle dégénéré peuvent être considérés comme des résultats valides

- Entrée: points alignés (3 ou plus)
  Résultat: à determiner, une erreur ou un triangle plat peuvent être considérés comme des résultats valides

Il me paraît difficile de tester avec une plus grande quantité de points car les différents algorithmes possibles procéderons à une triangulation différente.
On peut néanmoins tester des propriétés générales, comme le fait que chaque point doit appartenir à au moins un triangle, ou le fait qu'au maximum 2 triangles peuvent partager les deux même points.

## Tests d'intégration

Ces tests vérifie tout ce qui est relatif à la communication entre le client, le `Triangluator` et le `PointSetManager`

- Entrée: requête avec un `PointSetID` quelconque (valide ou non)
  MOC: `PointSetManager` qui renvoie une erreur 400
  Résultat: erreur 400, même données d'erreur que renvoyé par le MOC

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` qui renvoie une erreur 404
  Résultat: erreur 404, même données d'erreur que renvoyé par le MOC

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` qui renvoie un `PointSet` invalide (mauvais format)
  Résultat: erreur 500, avec un message d'erreur

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` injoinable (timeout ou autre erreur réseau)
  Résultat: erreur 503, avec un message d'erreur

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` qui renvoie une erreur 503
  Résultat: erreur 503, même données d'erreur que renvoyé par le MOC ?

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` qui renvoit un `PointSet` avec moins de 3 points
  Résultat: erreur 500, avec un message d'erreur

- Entrée: requête avec un `PointSetID` valide
  MOC: `PointSetManager` qui renvoit un `PointSet` valide
  Résultat: un résultat de triangulation valide

## Tests de performance

La sérialisation / désérialisation et la triangulation seront testés de manière indépendante.
Le sérialisation et désérialisation seront testés avec des grosse quantités de points et de triangles.
La triangulation sera testée de manière similaire avec beaucoup de points.
Les quantitées de données avec lequelles tester seront déterminées selon les performances des implémentations initialles, mais une base de 10 000 ou 100 000 paraît initialement raisonnable.