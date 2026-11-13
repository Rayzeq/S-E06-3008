# Retour d'expérience

## Évolution des tests

Lors de l'implémentation, beaucoup de tests ont évolué pour différentes raisons, certaines qui étaient prévisibles à l'avance, d'autres non. J'en fait ici la liste complète.

1. **Tests d'intégration HTTP**: j'ai initialement implémenté ces tests en utilisant `unittest.mock.patch`. Je ne m'étais pas rendu compte qu'en faisant ça, je remplaçais aussi la méthode `get` utilisée dans le test lui-même, ce qui veut dire que les tests n'appelaient en réalité jamais le code du service. Le passage à la bibliothèque `responses` a permis de résoudre ce problème.
2. **Tests de désérialisation**: lors de l'implémentation j'ai dû prendre une décision sur un aspect qui n'était pas spécifié dans les consignes: l'endianness des données binaires. J'avais, dès le début, prévu de tout implémenter en little-endian, mais j'ai involontairement écrit les floats en big-endian dans mon plan de test, j'ai donc corrigé ce problème quand je m'en suis rendu compte lors de l'implémentation.
3. **Test de sérialisation**: j'ai ajouté un test de sérialisation avec plusieurs triangles pour plus de robustesse.
4. **Tests de triangulation**: quand j'ai écrit les tests, je ne savais pas vraiment comment marchait les algorithmes de triangulation, je ne savais donc pas vraiment comment gérer les points confondus ou alignés, j'avais donc explicitement décidé de ne pas définir ce comportement. Après avoir implémenté la triangulation, j'ai pris la décision que ces cas causeraient une erreur.
5. **Tests de triangulation**: lors de l'implémentation, j'ai ajouté une nouvelle fonction que je n'avais pas prévu: `in_circumcircle`. J'ai donc dû ajouter des tests pour cette méthode.
6. **Tests de triangulation**: comme un variation du test des points confondus, j'ai ajouté un test dans le cas où il y a 4 points dont 2 confondus (dupliqués). Au vu de l'algorithme de triangulation, il était cohérent que ce cas soit accepté, avec un seul triangle comme résultat.
7. **Tests d'intégration**: lors de l'écriture du test qui vérifiait un comportement entièrement fonctionnel, je ne savais pas dans quel ordre les points seraient retournés par l'algorithme. J'ai donc dû changer l'ordre des points. Je ne suis pas certain de la pertinence de ce test sous cette forme, puisqu'un changement valide de l'algorithme de triangulation pourrait l'empêcher de passer, mais désérialiser les points dans le test ne me paraissait pas être une bonne idée non plus, car cela reviendrait à aussi tester la fonction de désérialisation.
8. **Tests de performance**: ceux-ci étaient vaguement définis dans le plan initial. Ils ont été précisés au moment de les écrire pour de vrai. Plus d'informations sont disponibles dans la partie dédiée.

Dans l'ensemble je pense que le plan était plutôt bon. Les tests de triangulation ont beaucoup du changer car je ne savais pas encore quel algorithme j'utiliserais, il aurait peut-être été judicieux de plus étudier les options disponibles et en choisir une au moment de l'écriture du plan afin de proposer des tests plus pertinents.

**Note sur la couverture des tests**: les tests ne couvrent pas 100% du code: il manque une ligne, qui est `app.run(host="0.0.0.0", port=5000)` dans le fichier `main.py`. Tester cette ligne n'aurait pas de sens puisque cela impliquerait de lancer le vrai serveur.

## Tests de performance

Dans le plan initial je n'avais pas choisis le nombre de données à utiliser pour les tests de performance (si ce n'est deux nombre donnés plus ou moins au hasard). Lors de l'écriture de ces tests j'ai donc vérifié la performance de chaque fonction pour pouvoir utiliser des chiffres cohérent. J'ai décidé de tester 3 quantités différentes par tests: le maximum étant une quantité qui donne des résultats de l'ordre de la seconde sur ma machine, puis les 2 autres descendant à partir de là, afin de se rendre compte de la linéarité, ou non, de ces fonctions.

Voici les résultats observés sur ma machine:

|         Test          | Nombre d'éléments | Temps d'exécution |
|-----------------------|-------------------|-------------------|
| serialize_triangles   | 10000             | 0.0611s           |
| serialize_triangles   | 20000             | 0.4260s           |
| serialize_triangles   | 30000             | 4.2163s           |
| deserialize_point_set | 10000             | 0.0055s           |
| deserialize_point_set | 100000            | 0.0735s           |
| deserialize_point_set | 1000000           | 1.5064s           |
| triangulate (random)  | 100               | 0.0191s           |
| triangulate (random)  | 500               | 0.3917s           |
| triangulate (random)  | 1000              | 1.2625s           |
| triangulate (grid)    | 100               | 0.0159s           |
| triangulate (grid)    | 400               | 0.3139s           |
| triangulate (grid)    | 900               | 1.8878s           |

Comme on peut le voir n'a vraiment des performances linéaires, mais la pire d'entre toutes est la sérialisation. Cela est sans doute dû aux nombreuses copies de données effectuées durant cette opération.
La triangulation semble quadratique, ce qui n'est pas vraiment surprenant.
