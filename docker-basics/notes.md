# Docker - Notes

## Container vs virtual machine

- A **VM** runs a full operating system with its **own kernel** (e.g. Hyper-V VMs). Heavy: GBs, boots in about a minute.
- A **container** **shares the host's kernel** and only packages the application and its dependencies. Light: MBs, starts in a second.
- Proof: `uname -r` gives the same kernel version inside a container and on the host.

## Image vs container

- **Image**: a read-only template (like a **class**).
- **Container**: a running instance created from an image (like an **object**). One image can give many containers.
- Each `docker run` creates a **new** container.

## Architecture

- **Client** (`docker` command): sends requests.
- **Daemon** (`dockerd`): background service on the host that does the work (pulls images, creates and runs containers). The client talks to its API through `/var/run/docker.sock`.
- **Registry** (Docker Hub): remote library of images.
- Being in the `docker` group is almost equivalent to being **root** on the host.

## Commands

```bash
docker run hello-world             # create and start a container
docker run -it --rm ubuntu bash    # interactive shell, container deleted on exit
docker images                      # list local images
docker ps                          # running containers
docker ps -a                       # all containers, including stopped ones
docker rm <id>                     # delete a stopped container
docker container prune             # delete all stopped containers
```

- `-i`: keep input open. `-t`: allocate a terminal. `--rm`: delete the container when it stops.
- The `STATUS` column shows the exit code: `Exited (0)` = success, `Exited (127)` = command not found.

## Containers are disposable

Anything written **inside** a container disappears with it. A new `docker run` starts from the image, which never contains those changes.

## Bind mounts

```bash
docker run -it --rm -v "$PWD":/work ubuntu bash
```

- `-v host_path:container_path`: the **same** folder seen from two places. No copy: changes are visible on both sides, and survive the container.
- Processes run as **root** by default: files they create on the host belong to root.
- Run as your own user instead:

```bash
docker run -it --rm -v "$PWD":/work --user "$(id -u):$(id -g)" ubuntu bash
```

- Linux identifies users by **number** (UID). Names come from each system's `/etc/passwd`: UID 1000 can be `ubuntu` in the container and `cytech` on the host, it is the same user for the kernel.
