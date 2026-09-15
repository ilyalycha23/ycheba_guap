create table подразделение (
    ид int primary key,
    наименование varchar(200) not null,
    ид_родительское int null,
    check (ид is distinct from ид_родительское),
    foreign key (ид_родительское) references подразделение (ид) on delete no action on update cascade
);

create table должность (
    ид int primary key,
    наименование varchar(150) not null unique,
    категория varchar(20) not null check (категория in ('инженер', 'техник', 'прочее'))
);

create table штатное_расписание (
    ид int primary key,
    ид_подразделения int not null,
    ид_должности int not null,
    количество_единиц smallint not null check (количество_единиц > 0),
    unique (ид_подразделения, ид_должности),
    foreign key (ид_подразделения) references подразделение (ид) on delete no action on update cascade,
    foreign key (ид_должности) references должность (ид) on delete no action on update cascade
);

create table сотрудник (
    ид int primary key,
    фио varchar(200) not null,
    дата_рождения date null
);

create table дети (
    ид int primary key,
    ид_сотрудника int not null,
    фио varchar(200) not null,
    пол char(1) not null check (пол in ('М', 'Ж')),
    дата_рождения date null,
    foreign key (ид_сотрудника) references сотрудник (ид) on delete no action on update cascade
);

create table прием (
    ид int primary key,
    ид_сотрудника int not null,
    ид_подразделения int not null,
    ид_должности int not null,
    дата_приема date not null,
    совместительство bit(1) not null default '0'::bit(1),
    foreign key (ид_сотрудника) references сотрудник (ид) on delete no action on update cascade,
    foreign key (ид_подразделения) references подразделение (ид) on delete no action on update cascade,
    foreign key (ид_должности) references должность (ид) on delete no action on update cascade
);

create table перевод (
    ид int primary key,
    ид_сотрудника int not null,
    ид_подразделения_откуда int not null,
    ид_подразделения_куда int not null,
    дата_перевода date not null,
    ид_новой_должности int null,
    check (ид_подразделения_откуда is distinct from ид_подразделения_куда),
    foreign key (ид_сотрудника) references сотрудник (ид) on delete no action on update cascade,
    foreign key (ид_подразделения_откуда) references подразделение (ид) on delete no action on update cascade,
    foreign key (ид_подразделения_куда) references подразделение (ид) on delete no action on update cascade,
    foreign key (ид_новой_должности) references должность (ид) on delete no action on update cascade
);

create table увольнение (
    ид int primary key,
    ид_сотрудника int not null,
    дата_увольнения date not null,
    foreign key (ид_сотрудника) references сотрудник (ид) on delete no action on update cascade
);