create table if not exists facility
(
    id    serial  not null
        constraint facilities_pk
            primary key,
    name  text    not null,
    level integer not null,
    pax   integer not null
);

alter table facility
    owner to likz;

create unique index if not exists facilities_id_uindex
    on facility (id);

create unique index if not exists facilities_name_uindex
    on facility (name);

create table if not exists booking
(
    booking_id   serial not null
        constraint booking_pk
            primary key,
    start_time   timestamp,
    end_time     timestamp,
    booked_by    text,
    facility_id  integer
        constraint booking_facility_id_fk
            references facility,
    booking_name text
);

alter table booking
    owner to likz;

create unique index if not exists booking_booking_id_uindex
    on booking (booking_id);

create unique index if not exists booking_booking_id_uindex_2
    on booking (booking_id);
