from github_etl.warehouse import Warehouse

class Analytics:
    def __init__(self, warehouse: Warehouse):
        self._warehouse = warehouse