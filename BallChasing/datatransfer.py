from networktables import NetworkTables

class datatransfer():
        def __init__(self, ip, table_name):
                self.NetworkTables.initialize(server = ip)
                self.table = self.NetworkTables.getTable(table_name)
        def send(self, name, value):
                self.table.putNumber(name, value)
        def get(self, name):
                return self.table.getNumber(name)

