CREATE TABLE rates (
  rate_id int(11) NOT NULL AUTO_INCREMENT,
  date DATE NOT NULL,
  currency_code tinyint(3) NOT NULL,
  rate varchar(100) NOT NULL,
  base varchar(100) DEFAULT 'USD',
  PRIMARY KEY (rate_id)
)

