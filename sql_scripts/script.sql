create table if not exists gt.facility
(
    id    serial  not null
        constraint facilities_pk
            primary key,
    name  text    not null,
    level integer not null,
    pax   integer not null
);

alter table gt.facility
    owner to likz;

create unique index if not exists facilities_id_uindex
    on gt.facility (id);

create unique index if not exists facilities_name_uindex
    on gt.facility (name);

create table if not exists gt.fb_user
(
    user_id serial not null,
    name    text   not null
);

alter table gt.fb_user
    owner to likz;

create table if not exists gt.booking
(
    booking_id  serial not null
        constraint booking_pk
            primary key,
    start_time  timestamp,
    end_time    timestamp,
    booked_by   text
        constraint booking_user_name_fk
            references gt.fb_user (name),
    facility_id integer
        constraint booking_facility_id_fk
            references gt.facility,
    name        text
);

alter table gt.booking
    owner to likz;

create unique index if not exists booking_booking_id_uindex
    on gt.booking (booking_id);

create unique index if not exists booking_booking_id_uindex_2
    on gt.booking (booking_id);

create unique index if not exists user_name_uindex
    on gt.fb_user (name);

create unique index if not exists user_user_id_uindex
    on gt.fb_user (user_id);

