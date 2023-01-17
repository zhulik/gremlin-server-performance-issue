import asyncio
import uuid
import random
import timeit
import time

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

graph = Graph()

def connect(port):
    connstring = f"ws://gremlin-server-{version}:8182/gremlin"
    return DriverRemoteConnection(connstring, 'g')

def test(version):
    conn = connect(version)
    g = graph.traversal().withRemote(conn)
    g.V().drop().iterate()
    
    # Array of 100 arrays, 100 longs in each
    batches = [ [ statics.long(n) for n in range(100) ] for _ in range(100) ]

    for batch in batches:
        x = g    
        for id in batch:
            # The addV part can be removed, in this case the performance difference won't be
            # so dramatic, but still be pretty much noticeable
            x = x.V(id).fold().coalesce(__.unfold(), __.addV("test").property(T.id, id))
        x.iterate()
    
    conn.close()

print("Sleep 5 seconds to let gremlin server start as it doesn't have healthchecks")
time.sleep(5) 

for version in ["3.5.3", "3.5.4"]:
    print(f"{version} =", timeit.timeit(f"test(\"{version}\")", number=1, globals=globals()))
