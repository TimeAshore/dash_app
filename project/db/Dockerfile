# base image
FROM postgres:11.1-alpine

# run init.sh on init
ADD init.sh /docker-entrypoint-initdb.d
RUN chmod 755 /docker-entrypoint-initdb.d/init.sh

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

################## 注意事项 ##################
# init.sh 只会在PG第一次初始化的时候执行，官网说明如下：
# Warning: scripts in /docker-entrypoint-initdb.d are only run
#          if you start the container with a data directory that
#          is empty; any pre-existing database will be left
#          untouched on container startup. One common problem is
#          that if one of your /docker-entrypoint-initdb.d scripts
#          fails (which will cause the entrypoint script to exit)
#          and your orchestrator restarts the container with the
#          already initialized data directory, it will not continue
#          on with your scripts.
# 具体操作如下：
# 1. 首先停止并删除对应镜像的容器(socamas-db)
# docker-compose rm socamas-db
# 2. 在镜像所在文件夹下添加空文件夹(data/), 并在对应docker-compose修改对应镜像的配置
# socamas-db:
#    build:
#      context: ./services/socamas/project/db
#      dockerfile: Dockerfile
#    ports:
#      - 5435:5432
#    environment:
#      - POSTGRES_USER=xxx
#      - POSTGRES_PASSWORD=xxx
#      - POSTGRES_DB=xxx
#    volumes:
#      - ./data/postgres:/var/lib/postgresql/data
# 3. 重新进行构建 docker-compose up --build
# 4. 删除刚才在镜像文件夹下添加的空文件夹(data/), 并删除刚才添加的相关配置
# 5. 再次重新构建并启动容器
# 参考链接地址：
# (1) https://github.com/docker-library/postgres/issues/203
# (2) https://docs.docker.com/samples/library/postgres/
