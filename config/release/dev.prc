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

# DClass files (in reverse order):
dc-file astron/dclass/united.dc

# Core features:
want-pets #t
want-parties #t
want-cogdominiums #t
want-lawbot-cogdo #t
want-achievements #f
want-anim-props #t
want-game-tables #t
want-find-four #t
want-chinese-checkers #t
want-checkers #t

# Chat:
want-whitelist #f

# Optional:
want-jor-el-cam #f

# Developer options:
show-population #t
want-instant-parties #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5