# This is the PRC configuration file for a published TTStride client. Note that only
# this file and Panda3D's Confauto.prc are included. Any relevant directives in
# Config.prc should be reproduced here.

# Client settings
window-title Toontown Stride [Alpha]
server-version SERVER_VERSION_HERE
video-library-name p3ffmpeg
want-dev #f
preload-avatars #t

# Graphics:
aux-display pandagl
aux-display pandadx9
aux-display p3tinydisplay


# Textures:
texture-anisotropic-degree 16


# Resources settings
model-path /
model-cache-models #f
model-cache-textures #f
vfs-mount resources/default/phase_3.mf /
vfs-mount resources/default/phase_3.5.mf /
vfs-mount resources/default/phase_4.mf /
vfs-mount resources/default/phase_5.mf /
vfs-mount resources/default/phase_5.5.mf /
vfs-mount resources/default/phase_6.mf /
vfs-mount resources/default/phase_7.mf /
vfs-mount resources/default/phase_8.mf /
vfs-mount resources/default/phase_9.mf /
vfs-mount resources/default/phase_10.mf /
vfs-mount resources/default/phase_11.mf /
vfs-mount resources/default/phase_12.mf /
vfs-mount resources/default/phase_13.mf /
default-model-extension .bam


# DC files are NOT configured.
# They're wrapped up into the code automatically.


# Core features:
want-pets #t
want-parties #f
want-cogdominiums #t
want-anim-props #t
want-game-tables #t
want-find-four #t
want-chinese-checkers #t
want-checkers #t
want-house-types #t
want-gifting #t
want-top-toons #t
want-language-selection #t
estate-day-night #t
want-mat-all-tailors #t


# Temporary:
smooth-lag 0.4
want-old-fireworks #t


# Developer options:
want-dev #f
want-pstats 0


# Chat:
want-whitelist #f
want-sequence-list #f

want-emblems #t
cogdo-want-barrel-room #t


#<dev>
show-total-population #t
want-instant-parties #t
want-instant-delivery #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5
default-directnotify-level info

# Core features:
want-lawbot-cogdo #t

# Crates:
dont-destroy-crate #t
get-key-reward-always #t
get-crate-reward-always #t
#</dev>

#<prod>
dont-destroy-crate #f
get-key-reward-always #f
get-crate-reward-always #f
want-lawbot-cogdo #f
#</prod>

