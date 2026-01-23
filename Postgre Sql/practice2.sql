create table bottle(
	id int, 
	name varchar(50),
	age int,
	city varchar(50)
);

insert into bottle(id, name, age, city) 
values 
(102, 'manish', 18, 'pat'),
(103, 'aasha', 20, 'hajipur')
, (104, 'manish', 21, 'cheenai');

select * from bottle;

update bottle set city='patna'
where id = 102;

update bottle set age = 20
where name = 'ganpat';

delete from bottle where id = 104;