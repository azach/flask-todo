drop table if exists tasks;
create table tasks (
  id integer primary key autoincrement,
  text text not null,
  completed boolean not null
);
