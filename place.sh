#!/bin/bash
rsync -r --exclude '*.sh' --exclude '*~' --exclude '*git' . root@9.126.113.160:/usr/share/pyshared/swift &
rsync -r --exclude '*.sh' --exclude '*~' --exclude '*git' . root@9.126.113.161:/usr/share/pyshared/swift &
rsync -r --exclude '*.sh' --exclude '*~' --exclude '*git' . root@9.109.124.109:/usr/share/pyshared/swift &
rsync -r --exclude '*.sh' --exclude '*~' --exclude '*git' . root@9.109.124.110:/usr/share/pyshared/swift &