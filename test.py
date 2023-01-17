import asyncio
import uuid
import random
import timeit

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import T, P, Operator
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

IDS = list(range(10000000,10000020))
NODES = [ statics.long(random.choice(IDS)) for _ in range(10_000) ]
BATCHES = [NODES[i:i + 100] for i in range(0, len(NODES), 100)]

graph = Graph()

def connect(port):
    connstring = f"ws://127.0.0.1:{port}/gremlin"
    return DriverRemoteConnection(connstring, 'g')

def test(port):
    conn = connect(port)
    g = graph.traversal().withRemote(conn)
    g.V().drop().iterate()
    
    for batch in BATCHES:
        x = g    
        for id in batch:
            (
                x := x.V(id)
                    .fold()
                    .coalesce(
                        __.unfold(),
                        __.addV("test").property(T.id, id)
                    )
            )
        x.iterate()
    
    g = graph.traversal().withRemote(conn)
    conn.close()

for v in ["353", "354"]:
    print(f"{v} = ", timeit.timeit(f"test({v})", number=1, globals=globals()))
