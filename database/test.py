from database.DAO import DAO

dao = DAO()
edges = dao.get_edges("disk", 2004)
for edge in edges:
    print(edge)
