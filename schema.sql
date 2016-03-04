DROP TABLE IF EXISTS log;

-- do not collect identifiable information
CREATE TABLE log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  system VARCHAR(20) not NULL,
  node VARCHAR(20),
  release VARCHAR(50),
  machine VARCHAR(20) not NULL,
  processor VARCHAR(5) not NULL,
  version VARCHAR(50) not NULL,
  time VARCHAR(30) not NULL
);

