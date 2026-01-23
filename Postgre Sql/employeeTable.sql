create table employee(
	emp_id serial primary key,
	fname varchar(30) not null,
	lname varchar(30) not null,
	email varchar(50) not null unique,
	dept varchar(30),
	salary decimal(10,2) default 30000.00,
	hire date not null default current_date
);

select * from employee;

INSERT INTO employee (fname, lname, email, dept, salary)
VALUES ('Amit', 'Sharma', 'amit.sharma@company.com', 'IT', 55000)
RETURNING emp_id;

INSERT INTO employee (fname, lname, email)
VALUES ('Neha', 'Verma', 'neha.verma@company.com');


