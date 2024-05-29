pip install yoyo-migrations
yoyo init --database postgresql://authenticator:xxxx@localhost:5432/postgres migrations
yoyo list
yoyo apply
yoyo rollback
