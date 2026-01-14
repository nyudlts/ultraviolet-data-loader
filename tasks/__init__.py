import urllib3
from invoke import Collection

from tasks import records, core, communities

# This is to avoid errors when testing on local instance with self-signed certificate
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

ns = Collection(initialize=core.initialize)
ns.add_collection(records)
ns.add_collection(communities)
