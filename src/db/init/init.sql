CREATE TABLE authors(
   author_id SERIAL,
   name VARCHAR(255)  NOT NULL,
   bio TEXT,
   birth_date DATE,
   birth_location VARCHAR(255) ,
   last_scrap_version TEXT NOT NULL,
   PRIMARY KEY(author_id),
   UNIQUE(name)
);

CREATE TABLE tags(
   tag_id SERIAL,
   libelle VARCHAR(100)  NOT NULL,
   PRIMARY KEY(tag_id),
   UNIQUE(libelle)
);

CREATE TABLE books(
   book_id SERIAL,
   title VARCHAR(255)  NOT NULL,
   price NUMERIC(8,2)  ,
   mark SMALLINT,
   availability BOOLEAN NOT NULL,
   img_url VARCHAR(255) ,
   last_scrap_version TEXT NOT NULL,
   author_id INTEGER NOT NULL,
   PRIMARY KEY(book_id),
   UNIQUE(title),
   FOREIGN KEY(author_id) REFERENCES authors(author_id)
);

CREATE TABLE book_stores(
   book_store_id SERIAL,
   name VARCHAR(255)  NOT NULL,
   address VARCHAR(255) ,
   zip_code VARCHAR(50) ,
   city VARCHAR(50) ,
   latitude NUMERIC(9,6)  ,
   longitude NUMERIC(9,6)  ,
   contact_name_hash VARCHAR(255) ,
   contact_email_hash VARCHAR(255) ,
   contact_phone VARCHAR(255) ,
   revenues_crypt NUMERIC(15,2)  ,
   partner_date DATE,
   speciality VARCHAR(255) ,
   PRIMARY KEY(book_store_id),
   UNIQUE(name)
);

CREATE TABLE quotes(
   quote_id SERIAL,
   text_content TEXT NOT NULL,
   last_scrap_version SMALLINT NOT NULL,
   author_id INTEGER NOT NULL,
   PRIMARY KEY(quote_id),
   UNIQUE(text_content),
   FOREIGN KEY(author_id) REFERENCES authors(author_id)
);

CREATE TABLE quote_tags(
   quote_id INTEGER,
   tag_id INTEGER,
   PRIMARY KEY(quote_id, tag_id),
   FOREIGN KEY(quote_id) REFERENCES quotes(quote_id),
   FOREIGN KEY(tag_id) REFERENCES tags(tag_id)
);

CREATE TABLE sells(
   book_id INTEGER,
   book_store_id INTEGER,
   PRIMARY KEY(book_id, book_store_id),
   FOREIGN KEY(book_id) REFERENCES books(book_id),
   FOREIGN KEY(book_store_id) REFERENCES book_stores(book_store_id)
);
