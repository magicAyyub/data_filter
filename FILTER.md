# Filter

La classe Filter offre des méthodes statiques pour filtrer une liste d'objets de type Data en fonction de critères spécifiques. Ces méthodes facilitent la création de filtres flexibles et personnalisés pour répondre à différents besoins de filtrage.

## Méthodes de filtrage disponibles

### filter_by_string_lexicographical

Filtre les données en fonction d'une comparaison lexicographique d'une valeur de type chaîne de caractères associée à une clé spécifique.

```python
Filter.filter_by_string_lexicographical(data_list: List[Data], key: str, value: str) -> List[Data]
```

### filter_by_string_contains

Filtre les données en fonction de la présence d'une sous-chaîne dans une valeur de type chaîne de caractères associée à une clé spécifique.

```python
Filter.filter_by_string_contains(data_list: List[Data], key: str, substring: str) -> List[Data]
```

### filter_by_string_starts_with

Filtre les données en fonction du début d'une valeur de type chaîne de caractères associée à une clé spécifique.

```python
Filter.filter_by_string_starts_with(data_list: List[Data], key: str, prefix: str) -> List[Data]
```

### filter_by_string_ends_with

Filtre les données en fonction de la fin d'une valeur de type chaîne de caractères associée à une clé spécifique.

```python
Filter.filter_by_string_ends_with(data_list: List[Data], key: str, suffix: str) -> List[Data]
```

### filter_by_list_all_elements

Filtre les données en fonction de la présence de tous les éléments d'une liste associée à une clé spécifique.

```python
Filter.filter_by_list_all_elements(data_list: List[Data], key: str, element: Any) -> List[Data]
```

### filter_by_list_min

Filtre les données en fonction de la valeur minimale d'une liste associée à une clé spécifique.

```python
Filter.filter_by_list_min(data_list: List[Data], key: str, min_value: Any) -> List[Data]
```

### filter_by_list_max

Filtre les données en fonction de la valeur maximale d'une liste associée à une clé spécifique.

```python
Filter.filter_by_list_max(data_list: List[Data], key: str, max_value: Any) -> List[Data]
```

### filter_by_list_average

Filtre les données en fonction d'une condition sur la moyenne des valeurs d'une liste associée à une clé spécifique.

```python
Filter.filter_by_list_average(data_list: List[Data], key: str, average_condition: Callable[[Any], bool]) -> List[Data]
```

### compare_fields

Filtre les données en comparant deux champs spécifiques.

```python
Filter.compare_fields(data_list: List[Data], field1: str, field2: str) -> List[Data]
```

### filter_by_global_statistics

Filtre les données en fonction d'une condition sur les statistiques globales d'une liste associée à une clé spécifique.

```python
Filter.filter_by_global_statistics(data_list: List[Data], key: str, condition: Callable[[Any], bool]) -> List[Data]
```

### filter_by_combined_fields

Filtre les données en fonction d'une combinaison de deux champs dépassant un seuil spécifique.

```python
Filter.filter_by_combined_fields(data_list: List[Data], field1: str, field2: str, threshold: Any) -> List[Data]
```

Absolument, clarifions l'utilisation du `Filter` dans la classe `DataSet` dans le README :


### Méthodes de filtrage dans DataSet

#### `filter_data`

La méthode `filter_data` prend une fonction de filtrage en tant que paramètre et renvoie une liste de données filtrées.

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

# Exemple d'utilisation :
dataset = DataSet()

# Filtrer les données où le champ "nom" contient la sous-chaîne "John"
filtered_data = dataset.filter_data(Filter.filter_by_string_contains, "nom", "John")
```

Cette méthode prend une fonction de filtrage de `Filter` en tant que premier argument et les arguments de filtrage supplémentaires en tant qu'arguments suivants. Cela offre une flexibilité pour appliquer différents filtres avec divers critères.
