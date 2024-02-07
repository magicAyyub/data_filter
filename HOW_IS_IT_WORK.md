Ci-dessous, Un exemple de chaque classe et expliqué comment elles pourraient être utilisées dans le projet. Le but est de donner un ordre d'idée pour voir comment chaque partie du projet communique avec les autres pour arriver au but fixé.

1. **Data** : Cette classe représente une seule entrée de données. Par exemple, si nous avons une entrée de données pour un étudiant avec un prénom, un nom, un âge, un statut d'apprenti et des notes, on peut créer une instance de `Data` pour cet étudiant :

   ````python
       data_dict = {"nom":"John", "lastname":"Doe", "age":20, "apprentice":True, "grades" = [12, 18, 14]}
       student = Data(data_dict)
   ```



3. **DataSet** : Cette classe contient une liste de `Data`. Nous pouvons ajouter des instances de `Data` à cette liste, puis utiliser les méthodes de `DataSet` pour manipuler ces données. Par exemple :

    ```python
    students = DataSet()
    students.add_data(student)  # Ajoute l'étudiant à la liste
    students.filter_data(age=20)  # Filtre les étudiants qui ont 20 ans
    students.sort_data()  # Trie les étudiants par ordre alphabétique du prénom
    ```



4. **Filter** : Cette classe est utilisée pour filtrer les données dans `DataSet`. Par exemple, si nous voulons filtrer les étudiants qui ont plus de 20 ans, on pourra créer une instance de `Filter` et l'appliquer à notre `DataSet` :

    ```python
    age_filter = Filter(threshold=20)
    students.filter_data(age_filter)
    ```



5. **Sorter** : Cette classe est utilisée pour trier les données dans `DataSet`. Par exemple, si nous voulons trier les étudiants par ordre alphabétique du prénom, vous pouvez créer une instance de `Sorter` et l'appliquer à votre `DataSet` :

    ```python
    name_sorter = Sorter()
    students.sort_data(name_sorter)
    ```



6. **Stats** : Cette classe est utilisée pour produire des statistiques à partir des données dans `DataSet`. Par exemple, si nous voulons calculer l'âge moyen des étudiants, on pourra créer une instance de `Stats` et l'appliquer à votre `DataSet` :

    ```python
    age_stats = Stats()
    average_age = age_stats.calculate_average(students, field="age")
    ```



7. **Interface** : Cette classe gère l'interaction avec l'utilisateur. Par exemple, elle pourrait avoir une méthode pour demander à l'utilisateur quelles opérations il souhaite effectuer sur les données :

    ```python
    interface = Interface()
    operation = interface.ask_user_operation()  # Demande à l'utilisateur quelle opération il souhaite effectuer
    interface.perform_operation(operation, students)  # Effectue l'opération sur les données
    ```



8. **History** : Cette classe gère l'historique des opérations de filtrage. Par exemple, après chaque opération de filtrage, nous pouvons ajouter l'état actuel des données à l'historique :

    ```python
    history = History()
    history.add_to_history(students.data_list)
    ```
