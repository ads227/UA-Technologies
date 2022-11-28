create table event (
    eventid int GENERATED ALWAYS AS IDENTITY,
    title text,
    category text,
    hours real,
    date date,
    facilityName text,
    facilityArea text,
    overhead real,
    rentalFee real,
    primary key(eventid)
);

create table department (
    departmentid int GENERATED ALWAYS AS IDENTITY,
    department text,
    ytdearnings real,
    primary key(departmentid)
);

create table eventstaffing (
    departmentid integer,
    eventid integer,
    staff integer,
    earnings real,
    primary key(departmentid, eventid),
    constraint dep_fk foreign key(departmentid) references department(departmentid),
    constraint ev_fk foreign key(eventid) references event(eventid)
);

alter table eventStaffing
    drop constraint dep_fk,
    add constraint dep_fk foreign key(departmentid) references department(departmentid) on delete cascade,
    drop constraint ev_fk,
    add constraint ev_fk foreign key(eventid) references event(eventid)on delete cascade;
