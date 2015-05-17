# Distribution:
distribution dev

# Art assets:
model-path ../resources/

# Server:
server-version tts-dev
min-access-level 600
accountdb-type developer
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass file:
dc-file astron/dclass/stride.dc

# Core features:
want-pets #t
want-parties #t
want-cogdominiums #t
want-lawbot-cogdo #t
want-anim-props #t
want-game-tables #t
want-find-four #t
want-chinese-checkers #t
want-checkers #t
want-house-types #t

# Chat:
want-whitelist #f

# Optional:
want-jor-el-cam #f

# Developer options:
show-population #t
want-instant-parties #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5
default-directnotify-level info
