CREATE TABLE 'modes' (mode_name   VARCHAR UNIQUE NOT NULL,
                      mode_id     VARCHAR UNIQUE NOT NULL       PRIMARY KEY,
                      description VARCHAR,
                      pce         NUMERIC        NOT NULL DEFAULT 0,
                      alpha       NUMERIC,
                      beta        NUMERIC,
                      gamma       NUMERIC,
                      delta       NUMERIC,
                      epsilon     NUMERIC,
                      zeta        NUMERIC,
                      iota        NUMERIC,
                      sigma       NUMERIC,
                      phi         NUMERIC,
                      tau         NUMERIC);

#
INSERT INTO 'modes' (mode_name, mode_id, description) VALUES('car', 'c', 'All motorized vehicles');
#
INSERT INTO 'modes' (mode_name, mode_id, description) VALUES('transit', 't', 'Public transport vehicles');
#
INSERT INTO 'modes' (mode_name, mode_id, description) VALUES('walk', 'w', 'Walking links');
#
INSERT INTO 'modes' (mode_name, mode_id, description) VALUES('bicycle', 'b', 'Biking links');

--@ Attributes follow
#
INSERT INTO 'attributes_documentation' (name_table, attribute, description) VALUES('modes','mode_name', 'The more descriptive name of the mode (e.g. Bycicle)');
#
INSERT INTO 'attributes_documentation' (name_table, attribute, description) VALUES('modes','mode_id', 'Single letter identifying the mode. E.g. b, for Bycicle');
#
INSERT INTO 'attributes_documentation' (name_table, attribute, description) VALUES('modes','description', 'Description of the same. E.g. Bycicles used to be human-powered two-wheeled vehicles');
