CREATE DATABASE pedraodb;

CREATE TABLE products (
	id 		SERIAL PRIMARY KEY,
	name  		VARCHAR(256),
	url 		VARCHAR(256),
	picture_path	VARCHAR(256),
	coupon		VARCHAR(64),
	category	VARCHAR(64),
	phrase		VARCHAR(512)
);

CREATE TABLE product_price (
	id 		SERIAL PRIMARY KEY,
	price 		FLOAT,
	date 		DATE,
	product_id	integer REFERENCES products(id)
);
