from invoke import Collection

from tasks import records, core, communities

ns = Collection(initialize=core.initialize)
ns.add_collection(records)
ns.add_collection(communities)
