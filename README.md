Tutorial being followed: blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Don't forget to run source venv/bin/activate


== docker startup ==
> docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=snowblunt_webb -e MYSQL_USER=snowblunt_webb \
    -e MYSQL_PASSWORD=<database-password> \
    mysql/mysql-server:5.7
> docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm \
    -e "discovery.type=single-node" \
    docker.elastic.co/elasticsearch/elasticsearch-oss:6.1.1
> docker run --name redis -d -p 6379:6379 redis:3-alpine
> docker run --name rq-worker -d --rm -e SECRET_KEY=my-secret-key \
    -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true \
    -e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \
    --link mysql:dbserver --link redis:redis-server \
    -e DATABASE_URL=mysql+pymysql://snowblunt_webb:<database-password>@dbserver/snowblunt_webb \
    -e REDIS_URL=redis://redis-server:6379/0 \
    --entrypoint venv/bin/rq \
    snowblunt_webb:latest worker -u redis://redis-server:6379/0 snowblunt_webb-tasks
> docker run --name snowblunt_webb -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
    -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true \
    -e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \
    --link mysql:dbserver --link redis:redis-server \
    -e DATABASE_URL=mysql+pymysql://snowblunt_webb:<database-password>@dbserver/snowblunt_webb \
    -e REDIS_URL=redis://redis-server:6379/0 \
    snowblunt_webb:latest

Debug
> docker logs snowblunt_webb
