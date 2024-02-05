#  Stats

La classe Stats offre des méthodes statiques pour générer des statistiques sur une liste d'objets de type Data. Ces méthodes permettent d'obtenir des informations utiles sur les champs de différentes natures, notamment les champs numériques, booléens et ceux représentant des listes.

## Méthodes disponibles dans la classe Stats

Les méthodes de statistiques disponibles sont :

- `generate_stats`: Génère des statistiques pour l'ensemble des champs de la liste de données.
- `generate_number_stats`: Génère des statistiques pour un champ numérique spécifique.
- `generate_boolean_stats`: Génère des statistiques pour un champ booléen spécifique.
- `generate_list_stats`: Génère des statistiques pour un champ représentant une liste.

## Fonctionnement des statistiques

La méthode `generate_stats` de la classe `Stats` prend une liste de données en tant qu'argument et génère des statistiques pour chaque champ, en distinguant les types de champs. Ces statistiques incluent le minimum, le maximum, la valeur moyenne pour les champs numériques, le pourcentage de valeurs vraies et fausses pour les champs booléens, ainsi que des statistiques sur la taille des listes pour les champs de type liste.

```python
class DataSet:

    def generate_stats(self) -> Dict[str, Dict[str, Union[float, int, Dict[Any, int]]]]:
        """Génère des statistiques pour l'ensemble des champs de la DataSet.

        Returns:
            Dict[str, Dict[str, Union[float, int, Dict[Any, int]]]]: Un dictionnaire contenant les statistiques pour chaque champ.
        """
        return Stats.generate_stats(self.data_list)
```

## Exemple d'utilisation des méthodes de statistiques dans DataSet :

```python
dataset = DataSet()

# Générer des statistiques pour l'ensemble des champs
all_fields_stats = dataset.generate_stats()

# Générer des statistiques pour le champ numérique "prix"
price_stats = dataset.generate_number_stats("prix")

# Générer des statistiques pour le champ booléen "disponible"
availability_stats = dataset.generate_boolean_stats("disponible")

# Générer des statistiques pour le champ de liste "tags"
tags_list_stats = dataset.generate_list_stats("tags")
```
