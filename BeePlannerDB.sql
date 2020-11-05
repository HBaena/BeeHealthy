DROP DATABASE IF EXISTS BeePlannerDB;
CREATE DATABASE BeePlannerDB;
USE BeePlannerDB;

CREATE TABLE User 
(
	user_id INT NOT NULL AUTO_INCREMENT,
	last_name NVARCHAR(25) NOT NULL,
	name NVARCHAR(20) NOT NULL,
	email NVARCHAR(30) NOT NULL,
	phone NVARCHAR(10) NOT NULL,
	password NVARCHAR(25) NOT NULL,
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE Activity
(
	activity_id INT NOT NULL AUTO_INCREMENT,
	name NVARCHAR(25) NOT NULL,
	priority INT NOT NULL,
	is_subject BOOLEAN NOT NULL,
	user_id INT NOT NULL REFERENCES User(user_id),
    start_time TIME NOT NULL,
    finish_time TIME NOT NULL,
	monday BOOLEAN NOT NULL,
	tuesday BOOLEAN NOT NULL,
	wednesday BOOLEAN NOT NULL,
	thursday BOOLEAN NOT NULL,
	friday BOOLEAN NOT NULL,
	saturday BOOLEAN NOT NULL,
	sunday BOOLEAN NOT NULL,	
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	PRIMARY KEY (activity_id)
);

CREATE TABLE Task
(
	task_id INT NOT NULL AUTO_INCREMENT,
	name NVARCHAR(20) NOT NULL,
	description NVARCHAR(30) NOT NULL,
	progress INT NOT NULL,	
	due_date DATETIME NOT NULL,
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	activity_id INT NOT NULL REFERENCES Activity(activity_id),
	PRIMARY KEY (task_id)
);

CREATE TABLE ListTask
(
	task_id INT NOT NULL REFERENCES Task(task_id),
    activity_id INT NOT NULL REFERENCES Task(activity_id),
	list_item NVARCHAR(20) NOT NULL,	
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	PRIMARY KEY (task_id, activity_id)
);

CREATE TABLE Reminder
(
	reminder_id INT NOT NULL AUTO_INCREMENT,
	name NVARCHAR(25) NOT NULL,
	description NVARCHAR(25) NOT NULL,
	reminder_date DATETIME NOT NULL,
	activity_id INT NOT NULL REFERENCES Activity(activity_id),
	is_all_day BOOLEAN NOT NULL,	
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	PRIMARY KEY (reminder_id)
);

CREATE TABLE Note
(
	note_id INT NOT NULL AUTO_INCREMENT,
	name NVARCHAR(25) NOT NULL,
	description NVARCHAR(30) NOT NULL,
	create_date DATETIME NOT NULL,
	modified_date DATETIME NOT NULL,
	activity_id INT NOT NULL REFERENCES Activity(activity_id),
	PRIMARY KEY(note_id)
);