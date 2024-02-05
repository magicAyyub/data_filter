# Sorter

La classe `Sorter` offre des methodes statiques pour trier d'objets de type `Data` en fonction de critères spécifiques. Ces méthodes facilitent la création de trie flexibles et personnalisés pour répondre à différents besoins. 


## Méthodes disponibles dans la classe Sorter

Les méthodes de trie disponible sont :

- `sort_by_field`
- `sort_by_multiple_fields`
- `sort_by_global_value`
- `sort_by_priority_criteria`

## Fonctionnement des filtre 

La méthode `sort_data` de la classe `DataSet` prend une fonction de trie de `Sorter` comme premier argument et les arguments de trie supplémentaires en tant qu'arguments suivants. Cela offre une flexibilité pour appliquer différents trie avec divers critères.

```python
class DataSet:

    def sort_data(self, sort_function: Callable[[List[Data]], List[Data]]) -> List[Data]:
        """Trie les Data dans DataSet en utilisant une fonction de trie.

        Args:
            sort_function (Callable[[List[Data]], List[Data]]): La fonction de trie à appliquer.

        Returns:
            List[Data]: A list of sorted data.
        """
        return sort_function(self.data_list)
```

## Exemple d'utilisation des méthodes de trie dans DataSet:

```python
dataset = DataSet()

# Trier les données par nom dans l'ordre croissant
sorted_data_name_asc = dataset.sort_data(Sorter.sort_by_field, "name")

# Trier les données par âge dans l'ordre décroissant
sorted_data_age_desc = dataset.sort_data(Sorter.sort_by_field, "age", reverse=True)

# Trier les données par score puis par âge
sorted_data_score_age = dataset.sort_data(Sorter.sort_by_multiple_fields, ["score", "age"])

# Tri personnalisé à l'aide d'une fonction de valeur (Ici trie par le nombre de caractère du champ "name")
sorted_data_custom = dataset.sort_data(Sorter.sort_by_global_value, "name", lambda x: len(x), reverse=True)

# Tri personnalisé avec critères multiplesTri personnalisé avec critères multiples
sorted_data_multiple_criteria = dataset.sort_data(Sorter.sort_by_priority_criteria, [
    lambda x: x.age,
    lambda x: x.score,
    lambda x: len(x.name)
])

```
