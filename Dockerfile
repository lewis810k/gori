FROM        gsh2448/gori-front
MAINTAINER  dev@azelf.com

EXPOSE      80
CMD ["supervisord", "-n"]