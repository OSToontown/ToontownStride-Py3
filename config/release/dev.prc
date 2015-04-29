# Distribution:
distribution dev

# Art assets:
model-path ../resources/

# Server:
server-version ttu-dev
min-access-level 600
accountdb-type developer
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass file:
dc-file astron/dclass/united.dc

# Core features:
want-pets #t
want-parties #t
want-cogdominiums #t
want-lawbot-cogdo #t
want-anim-props #f

# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Optional:
want-glove-npc #t

# Developer options:
show-population #t
want-instant-parties #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5