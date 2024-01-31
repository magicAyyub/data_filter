Ci-dessous, Un exemple de chaque classe et expliqué comment elles pourraient être utilisées dans le projet. Le but est de donner un ordre d'idée pour voir comment chaque partie du projet communique avec les autres pour arriver au but fixé.

1. **Data** : Cette classe représente une seule entrée de données. Par exemple, si vous avez une entrée de données pour un étudiant avec un prénom, un nom, un âge, un statut d'apprenti et des notes, vous pouvez créer une instance de `Data` pour cet étudiant :

    ```python
    student = Data(firstname="John", lastname="Doe", age=20, apprentice=True, grades=[15, 18, 14])
    ```



2. **DataSet** : Cette classe contient une liste de `Data`. Vous pouvez ajouter des instances de `Data` à cette liste, puis utiliser les méthodes de `DataSet` pour manipuler ces données. Par exemple :

    ```python
    students = DataSet()
    students.add_data(student)  # Ajoute l'étudiant à la liste
    students.filter_data(age=20)  # Filtre les étudiants qui ont 20 ans
    students.sort_data()  # Trie les étudiants par ordre alphabétique du prénom
    ```



3. **Filter** : Cette classe est utilisée pour filtrer les données dans `DataSet`. Par exemple, si vous voulez filtrer les étudiants qui ont plus de 20 ans, vous pouvez créer une instance de `Filter` et l'appliquer à votre `DataSet` :

    ```python
    age_filter = Filter(threshold=20)
    students.filter_data(age_filter)
    ```



4. **Sorter** : Cette classe est utilisée pour trier les données dans `DataSet`. Par exemple, si vous voulez trier les étudiants par ordre alphabétique du prénom, vous pouvez créer une instance de `Sorter` et l'appliquer à votre `DataSet` :

    ```python
    name_sorter = Sorter()
    students.sort_data(name_sorter)
    ```



5. **Stats** : Cette classe est utilisée pour calculer des statistiques sur les données dans `DataSet`. Par exemple, si vous voulez calculer l'âge moyen des étudiants, vous pouvez créer une instance de `Stats` et l'appliquer à votre `DataSet` :

    ```python
    age_stats = Stats()
    average_age = age_stats.calculate_average(students, field="age")
    ```



6. **Interface** : Cette classe gère l'interaction avec l'utilisateur. Par exemple, elle pourrait avoir une méthode pour demander à l'utilisateur quelles opérations il souhaite effectuer sur les données :

    ```python
    interface = Interface()
    operation = interface.ask_user_operation()  # Demande à l'utilisateur quelle opération il souhaite effectuer
    interface.perform_operation(operation, students)  # Effectue l'opération sur les données
    ```



7. **History** : Cette classe gère l'historique des opérations de filtrage. Par exemple, après chaque opération de filtrage, vous pouvez ajouter l'état actuel des données à l'historique :

    ```python
    history = History()
    history.add_to_history(students.data_list)
    ```
