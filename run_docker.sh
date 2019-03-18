#!/usr/bin/env bash
#
# Runs the lab environment in docker.
#

IMAGE=${IMAGE:-greatscottgadgets/hacking-usb}
COMMAND="${@:-bash}"


if [ -z $DISPLAY ]; then
    docker run -it --privileged \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        --volume="$(pwd):/work" \
    --device="/dev/usbmon*" \
        ${IMAGE} \
        ${COMMAND}
else

    # Grant access to the container's image, so the container can access local resources.
    CONTAINER_ID=$(docker ps -l -q)
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' ${CONTAINER_ID}`

    # Run our docker instance with access to the host display socket.
    docker run -it --privileged \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        --volume="$(pwd):/work" \
    --device="/dev/usbmon*" \
        ${IMAGE} \
        ${COMMAND}


fi;
