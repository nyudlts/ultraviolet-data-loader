from invoke import Collection

from tasks import records, core

ns = Collection(initialize=core.initialize)
ns.add_collection(records)
