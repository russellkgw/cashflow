drop table if exists assumptions;
create table assumptions (
  id integer primary key autoincrement,
  variable text not null,
  'value' decimal
);