#  Filter

La classe Filter offre des méthodes statiques pour filtrer une liste d'objets de type Data en fonction de critères spécifiques. Ces méthodes facilitent la création de filtres flexibles et personnalisés pour répondre à différents besoins de filtrage. 


## Méthodes disponibles dans la classe Filter

Les méthodes de filtrage disponible sont : 

- `filter_by_string_contains`
- `filter_by_string_starts_with`
- `filter_by_string_ends_with`
- `filter_by_list_all_elements`
- `filter_by_list_min`
- `filter_by_list_max`
- `filter_by_list_average`
- `compare_fields`
- `filter_by_global_statistics`.

## Fonctionnement du filtre 

La méthode `filter_data` prend une fonction de filtrage de `Filter` en tant que premier argument et les arguments de filtrage supplémentaires en tant qu'arguments suivants. Cela offre une flexibilité pour appliquer différents filtres avec divers critères.

```python
class DataSet:
    # ...

    def filter_data(self, filter_function: Callable[[List[Data]], List[Data]]) -> List[Data]:
        """Applique un filtre aux données de la DataSet.

        Args:
            filter_function (Callable[[List[Data]], List[Data]]): La fonction de filtrage à appliquer.

        Returns:
            List[Data]: Une liste de données filtrées.
        """
        return filter_function(self.data_list)
```


## Exemple d'utilisation des méthodes de filtrage dans DataSet :

```python
dataset = DataSet()

# Filtrer les données où le champ "nom" contient la sous-chaîne "John"
filtered_data = dataset.filter_data(Filter.filter_by_string_contains, "nom", "John")

# Filtrer les données où le champ "nom" contient la sous-chaîne "John"
filtered_data = dataset.filter_data(Filter.filter_by_string_contains, "nom", "John")

# Filtrer les données où le champ "description" commence par "Java"
filtered_data = dataset.filter_data(Filter.filter_by_string_starts_with, "description", "Java")

# Filtrer les données où la liste "tags" contient l'élément "Python"
filtered_data = dataset.filter_data(Filter.filter_by_list_all_elements, "tags", "Python")

# Filtrer les données où le champ "prix" est supérieur à 55
filtered_data = dataset.filter_data(Filter.filter_by_list_min, "prix", 55)

# Filtrer les données où la moyenne des notations est supérieure à 4.0
filtered_data = dataset.filter_data(Filter.filter_by_list_average, "notations", lambda x: sum(x)/len(x) > 4.0)

# Comparer les champs "prix" et "quantites" et filtrer les données où le produit est supérieur à 5000
filtered_data = dataset.filter_data(Filter.filter_by_combined_fields, "prix", "quantites", 5000)

```
