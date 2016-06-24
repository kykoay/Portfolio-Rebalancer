import sqlite3

conn = sqlite3.connect('portalloc.sqlite')
cur = conn.cursor()

cur.executescript(
'''
DROP TABLE IF EXISTS FTPORTFOLIO;
DROP TABLE IF EXISTS FT_CURRENCY_ID;

CREATE TABLE FTPORTFOLIO (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	tickers TEXT UNIQUE,
	quantity INTEGER,
	current_price_lc NUMERIC ,
	current_price_usd NUMERIC,
	cashind INTEGER,
	currency_id INTEGER,
	tickerportvalue NUMERIC,
	target_percentage NUMERIC,
	current_percentage NUMERIC,
	target_quantity INTEGER,
	delta INTEGER	);

CREATE TABLE FT_CURRENCY_ID (
	currency_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	Eng_Desc TEXT UNIQUE
	)


'''	)

cur.executescript(
'''
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('CSJ',1,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('HHF.TO',2,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('SPY',4,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('USMV',30,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VBR',13,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VCN.TO',25,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VEU',23,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VPL',6,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VSP.TO',7,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('VSS',5,1,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('XCS.TO',55,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('XCV.TO',10,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('XMV.TO',25,2,0);
INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind) VALUES ('ZEO.TO',25,2,0);

INSERT INTO FT_CURRENCY_ID (currency_id,Eng_Desc) VALUES (1,"USD");
INSERT INTO FT_CURRENCY_ID (currency_id,Eng_Desc) VALUES (2, "CAD");

'''
	)



conn.commit()
