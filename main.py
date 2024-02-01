from  dataManagement.dataset import DataSet 

def main():
    ds = DataSet()
    ds.load_json("./dataSource/test/test.json")
    print(ds._all_to_dict())
    

 