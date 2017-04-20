import argparse
import os
import subprocess
import sys

# Const
MODE_BASE = 'base'
MODE_BASE2 = 'base2'
MODE_DEBUG = 'debug'
MODE_PRODUCTION = 'production'
MODE_DOCKERHUB = 'dockerhub'
MODE_ORIGINAL = 'original'

IMAGE_BASE = 'gori-front-base'
IMAGE_BASE2 = 'gori-front-base2'
IMAGE_DEBUG = 'gori-front-debug'
IMAGE_PRODUCTION = 'gori-front-production'
IMAGE_DOCKERHUB = 'gori-front'
IMAGE_ORIGINAL = 'gori-origianl'

MAINTAINER = 'gsh2448@gmail.com'
DOCKERFILE_BASE = 'Dockerfile.base'
DOCKERFILE_BASE2 = 'Dockerfile.base2'
DOCKERFILE_DEBUG = 'Dockerfile.debug'
DOCKERFILE_PRODUCTION = 'Dockerfile.production'
DOCKERFILE_DOCKERHUB = 'Dockerfile'
DOCKERFILE_ORIGINAL = 'Dockerfile.original'

# ArgumentParser
parser = argparse.ArgumentParser(description='Build command')
parser.add_argument('-m', '--mode', type=str, default=MODE_DEBUG)
args = parser.parse_args()

# Paths
ROOT_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(ROOT_DIR, '.conf')
CONF_DOCKER_DIR = os.path.join(CONF_DIR, 'docker')

# Docker conf files
dockerfile_template = open(os.path.join(CONF_DOCKER_DIR, '00_template.docker')).read()
dockerfile_original = open(os.path.join(CONF_DOCKER_DIR, '00_original_gori.docker')).read()
dockerfile_base = open(os.path.join(CONF_DOCKER_DIR, '01_base.docker')).read()
dockerfile_base2 = open(os.path.join(CONF_DOCKER_DIR, '01_base2.docker')).read()
dockerfile_extra = open(os.path.join(CONF_DOCKER_DIR, '02_extra.docker')).read()
dockerfile_extra_dockerhub = open(os.path.join(CONF_DOCKER_DIR, '03_extra_dockerhub.docker')).read()

if args.mode == MODE_BASE:
    dockerfile = dockerfile_template.format(
        from_image='ubuntu:16.04',
        maintainer=MAINTAINER,
        base=dockerfile_base,
        extra=''
    )
    filename = DOCKERFILE_BASE
    imagename = IMAGE_BASE
elif args.mode == MODE_BASE2:
    dockerfile = dockerfile_template.format(
        from_image=IMAGE_BASE,
        maintainer=MAINTAINER,
        base=dockerfile_base2,
        extra=''
    )
    filename = DOCKERFILE_BASE2
    imagename = IMAGE_BASE2
elif args.mode == MODE_DEBUG:
    dockerfile = dockerfile_template.format(
        from_image=IMAGE_BASE2,
        maintainer=MAINTAINER,
        base='',
        extra=dockerfile_extra
    )
    filename = DOCKERFILE_DEBUG
    imagename = IMAGE_DEBUG
elif args.mode == MODE_PRODUCTION:
    dockerfile = dockerfile_template.format(
        from_image='ubuntu:16.04',
        maintainer=MAINTAINER,
        base=dockerfile_base,
        extra=dockerfile_extra
    )
    filename = DOCKERFILE_PRODUCTION
    imagename = IMAGE_PRODUCTION
elif args.mode == MODE_DOCKERHUB:
    dockerfile = dockerfile_template.format(
        from_image='gsh2448/gori-front',
        maintainer=MAINTAINER,
        base='',
        extra=dockerfile_extra_dockerhub,
    )
    filename = DOCKERFILE_DOCKERHUB
    imagename = IMAGE_DOCKERHUB
elif args.mode == MODE_ORIGINAL:
    dockerfile = dockerfile_template.format(
        from_image='ubuntu:16.04',
        maintainer=MAINTAINER,
        base=dockerfile_original,
        extra='',
    )
    filename = DOCKERFILE_ORIGINAL
    imagename = IMAGE_ORIGINAL
else:
    sys.exit('Mode invalid')

with open(os.path.join(ROOT_DIR, filename), 'wt') as f:
    f.write(dockerfile)

build_command = 'docker build --no-cache . -t {imagename} -f {filename}'.format(
    imagename=imagename,
    filename=filename
)
print('Docker build command: {}'.format(build_command))
subprocess.run(build_command, shell=True)