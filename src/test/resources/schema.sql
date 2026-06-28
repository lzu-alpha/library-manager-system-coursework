DROP TABLE IF EXISTS borrowingbooks;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS book_category;
DROP TABLE IF EXISTS dept;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
  admin_id INT AUTO_INCREMENT PRIMARY KEY,
  admin_name VARCHAR(20),
  admin_pwd VARCHAR(20),
  admin_email VARCHAR(20)
);

CREATE TABLE user (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(20),
  user_pwd VARCHAR(20),
  user_email VARCHAR(30)
);

CREATE TABLE dept (
  dept_id INT AUTO_INCREMENT PRIMARY KEY,
  dept_name VARCHAR(20)
);

CREATE TABLE book_category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(20)
);

CREATE TABLE book (
  book_id INT AUTO_INCREMENT PRIMARY KEY,
  book_name VARCHAR(20) NOT NULL,
  book_author VARCHAR(20),
  book_publish VARCHAR(20),
  book_category INT,
  book_price DOUBLE,
  book_introduction VARCHAR(100),
  CONSTRAINT fk_book_category FOREIGN KEY (book_category) REFERENCES book_category(category_id)
);

CREATE TABLE borrowingbooks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  book_id INT,
  date DATE,
  CONSTRAINT fk_borrow_user FOREIGN KEY (user_id) REFERENCES user(user_id),
  CONSTRAINT fk_borrow_book FOREIGN KEY (book_id) REFERENCES book(book_id)
);
