DROP TABLE IF EXISTS userlog;
create table userlog(
    id integer PRIMARY KEY autoincrement,
    name text not null,
    password text not null,
    nowphase integer not null
);
CREATE INDEX name_index ON userlog(name);
