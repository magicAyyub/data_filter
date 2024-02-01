# Projet Data Filter

## Répartition des tâches

### Ayouba : Gestion des données et opérations

1. **Data** : Créer la classe `Data` qui représente une seule entrée de données. Chaque entrée de données est comme une boîte contenant plusieurs informations.

    ```python
    class Data:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    ```

2. **DataSet** : Créer la classe `DataSet` qui contient une liste de `Data`. Ajouter des méthodes pour charger et sauvegarder les données.

    ```python
    class DataSet:
        def __init__(self):
            self.data_list = []

        def add_data(self, data):
            self.data_list.append(data)

        # À compléter : méthodes pour charger et sauvegarder les données
    ```

3. **Filter** : Créer la classe `Filter` qui est utilisée pour filtrer les données dans `DataSet`.

    ```python
    class Filter:
        def __init__(self, field, value):
            self.field = field
            self.value = value

        def apply(self, data):
            return getattr(data, self.field) == self.value
    ```

4. **Sorter** : Créer la classe `Sorter` qui est utilisée pour trier les données dans `DataSet`.

    ```python
    class Sorter:
        def __init__(self, field):
            self.field = field

        def apply(self, data_list):
            return sorted(data_list, key=lambda data: getattr(data, self.field))
    ```

5. **Stats** : Créer la classe `Stats` qui est utilisée pour calculer des statistiques sur les données dans `DataSet`.

    ```python
    class Stats:
        def calculate_average(self, data_list, field):
            total = sum(getattr(data, field) for data in data_list)
            return total / len(data_list)
    ```

### Noussayba : Interface utilisateur et historique

6. **Interface** : Créer la classe `Interface` qui gère l'interaction avec l'utilisateur. Ajouter des méthodes pour demander à l'utilisateur quelles opérations il souhaite effectuer et pour effectuer ces opérations sur les données.

    ```python
    class Interface:
        def __init__(self, dataset):
            self.dataset = dataset

        # À compléter : méthodes pour interagir avec l'utilisateur et effectuer des opérations sur les données
    ```

7. **History** : Si on a le temps, créer la classe `History` qui gère l'historique des opérations de filtrage.

    ```python
    class History:
        def __init__(self):
            self.history_list = []

        def add_to_history(self, data_list):
            self.history_list.append(list(data_list))  # Faire une copie de la liste pour éviter les modifications ultérieures
    ```

---
