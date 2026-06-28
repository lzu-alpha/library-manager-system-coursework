INSERT INTO admin (admin_id, admin_name, admin_pwd, admin_email)
VALUES (1, 'admin', '123456', 'admin@example.com');

INSERT INTO user (user_id, user_name, user_pwd, user_email)
VALUES
  (1, 'user1', '123456', 'user1@example.com'),
  (2, 'yxc', '123456', 'yxc@example.com'),
  (3, 'user2', '123456', 'user2@example.com');

INSERT INTO dept (dept_id, dept_name)
VALUES
  (1, '信息工程学院'),
  (2, '电子工程学院');

INSERT INTO book_category (category_id, category_name)
VALUES
  (1, '小说'),
  (2, '计算机'),
  (3, '历史');

INSERT INTO book (book_id, book_name, book_author, book_publish, book_category, book_price, book_introduction)
VALUES
  (1, '平凡的世界', '路遥', '北京出版社', 1, 88.0, '长篇小说'),
  (2, 'Java程序设计', '张三', '电子工业出版社', 2, 69.0, 'Java教材'),
  (3, '数据库系统', '李四', '清华大学出版社', 2, 59.0, '数据库教材');

INSERT INTO borrowingbooks (id, user_id, book_id, date)
VALUES
  (1, 1, 1, '2026-06-01'),
  (2, 2, 2, '2026-06-10');
