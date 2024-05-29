- создать тестовую инфру БД
```
create schema api;

create table api.todos (
  id serial primary key,
  done boolean not null default false,
  task text not null,
  due timestamptz
);

insert into api.todos (task) values
  ('finish tutorial 0'), ('pat self on back');
create role web_anon nologin;

grant usage on schema api to web_anon;
grant select on api.todos to web_anon;

create role authenticator noinherit login password 'xxxx';
grant web_anon to authenticator;


create role todo_user nologin;
grant todo_user  to authenticator;

grant usage on schema api to todo_user;
grant all on api.todos to todo_user;
grant usage, select on sequence api.todos_id_seq to todo_user;
```
- скачать и распаковать архив postgrest-v12.0.3-linux-static-x64.tar.xz
- создать и поправить конфиги postgrest.conf
- разрешить функции агрегации
```export PGRST_DB_AGGREGATES_ENABLED=True```
- запусить веб сервер
```./postgrest ./postgrest.conf```

- выполнить запросы
```
GET localhost:3000/todos
Accept: application/json

GET localhost:3000/todos?select=id.sum()
Accept: application/json
```
- create secret token
```
# Allow "tr" to process non-utf8 byte sequences
export LC_CTYPE=C

# read random bytes and keep only alphanumerics
echo "jwt-secret = \"$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c32)\"" >> postgrest.conf
```
- generate JWT https://jwt.io
```export TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidG9kb191c2VyIn0.45vW5-J8h4OqhfukUYfpyFeslvL5FZx77GvlGA9gKV4```
