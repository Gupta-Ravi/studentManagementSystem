

create table teachers(
    id integer primary key AUTOINCREMENT,
    name text not null,
    password text not null,
    isteacher boolean not null DEFAULT '0');

create table students(
    stuid integer primary key AUTOINCREMENT,
    name text not null,
    email text,
    marks integer,
    address text);