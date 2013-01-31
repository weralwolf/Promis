-- satellites
DROP TABLE IF EXISTS "satellites";
CREATE TABLE "satellites"
(
    "title" VARCHAR(255) NOT NULL ,
    "description" TEXT NOT NULL ,
    PRIMARY KEY ("title")
)
;

-- devices
DROP TABLE IF EXISTS "devices";
CREATE TABLE "devices"
(
    "title" VARCHAR(255) NOT NULL ,
    "description" TEXT NOT NULL ,
    "satellites_title" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("title")
)
;

-- sessions
DROP SEQUENCE IF EXISTS "sessions_seq";
CREATE SEQUENCE "sessions_seq";

DROP TABLE IF EXISTS "sessions";
CREATE  TABLE "sessions" 
(
    "id" INTEGER NOT NULL DEFAULT nextval ('"sessions_seq"') ,
    "ibegin" TIMESTAMP NOT NULL ,
    "iEnd" TIMESTAMP NOT NULL ,
    PRIMARY KEY ("id")
);

--measurament_points
DROP SEQUENCE IF EXISTS "measurement_points_seq";
CREATE SEQUENCE "measurement_points_seq";

DROP TABLE IF EXISTS "measurement_points";
CREATE  TABLE "measurement_points" 
(
    "id" INTEGER NOT NULL DEFAULT nextval ('"measurement_points_seq"') ,
    "time" DOUBLE PRECISION NOT NULL ,
    "sessions_id" INTEGER NOT NULL ,
    "latitude" DOUBLE PRECISION NULL ,
    "longitude" DOUBLE PRECISION NULL ,
    "altitude" DOUBLE PRECISION NULL ,
    PRIMARY KEY ("id") 
);

--channels
DROP TABLE IF EXISTS "channels";
CREATE  TABLE "channels" 
(
    "title" VARCHAR(255) NOT NULL ,
    "description" TEXT NOT NULL ,
    "sampling_frequency" DOUBLE PRECISION NULL ,
    "devices_title" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("title") 
);

--units

DROP TABLE IF EXISTS "units";
CREATE  TABLE "units" 
(
    "title" VARCHAR(255) NOT NULL ,
    "short_name" VARCHAR(45) ,
    "long_name" VARCHAR(45) ,
    "description" VARCHAR(45) ,
    PRIMARY KEY ("title") 
);

--parameters
DROP TABLE IF EXISTS "parameters" ;
CREATE  TABLE IF NOT EXISTS "parameters" (
    "title" VARCHAR(255) NOT NULL ,
    "units_title" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("title") 
);

--measurements
DROP SEQUENCE IF EXISTS "measurements_seq";
CREATE SEQUENCE "measurements_seq";

DROP TABLE IF EXISTS "measurements" ;
CREATE  TABLE IF NOT EXISTS "measurements" (
    "id" INTEGER NOT NULL DEFAULT nextval ('"measurements_seq"') ,
    "parameters_title" VARCHAR(255) NOT NULL ,
    "channels_title" VARCHAR(45) NOT NULL ,
    "measurement_points_id" INTEGER NOT NULL ,
    "marker" INTEGER NOT NULL ,
    "measurement" BYTEA NOT NULL ,
    "rError" BYTEA NULL DEFAULT NULL ,
    PRIMARY KEY ("id")
);

--sessions_options
DROP SEQUENCE IF EXISTS "sessions_options_seq";
CREATE SEQUENCE "sessions_options_seq";

DROP TABLE IF EXISTS "sessions_options" ;
CREATE  TABLE IF NOT EXISTS "sessions_options" (
    "id" INTEGER NOT NULL DEFAULT nextval ('"sessions_options_seq"') ,
    "sessions_id" INTEGER NOT NULL ,
    "title" VARCHAR(255) NOT NULL ,
    -- changed this field from "value"
    "sessions_options_value" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("id")
);

--channels_has_sessions
DROP TABLE IF EXISTS "channels_has_sessions" ;
CREATE  TABLE IF NOT EXISTS "channels_has_sessions" (
    "channels_title" VARCHAR(255) NOT NULL ,
    "sessions_id" INTEGER NOT NULL ,
    PRIMARY KEY ("channels_title", "sessions_id")
);

--parameters_has_parameters
DROP TABLE IF EXISTS "parameters_has_parameters" ;
CREATE  TABLE IF NOT EXISTS "parameters_has_parameters" (
    "parent_title" VARCHAR(255) NOT NULL ,
    "child_title" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("parent_title", "child_title") 
);


--channels_has_parameters
DROP TABLE IF EXISTS "channels_has_parameters" ;
CREATE  TABLE IF NOT EXISTS "channels_has_parameters" (
    "channels_title" VARCHAR(255) NOT NULL ,
    "parameters_title" VARCHAR(255) NOT NULL ,
    PRIMARY KEY ("channels_title", "parameters_title")
);




ALTER TABLE "devices" 

    ADD CONSTRAINT "fk_devices_satellites"
    FOREIGN KEY ("satellites_title") 
    REFERENCES "satellites" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;


ALTER TABLE "channels" 

    ADD CONSTRAINT "fk_channels_devices"
    FOREIGN KEY ("devices_title") 
    REFERENCES "devices" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;


ALTER TABLE "channels_has_sessions" 

    ADD CONSTRAINT "fk_channels_has_sessions_chanels"
    FOREIGN KEY ("channels_title") 
    REFERENCES "channels" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE,

    ADD CONSTRAINT "fk_channels_has_sessions_sessions"
    FOREIGN KEY ("sessions_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;


ALTER TABLE "measurement_points"

    ADD CONSTRAINT "fk_measurement_points_sessions"
    FOREIGN KEY ("sessions_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;

ALTER TABLE "sessions_options"

    ADD CONSTRAINT "fk_sessions_options_sessions"
    FOREIGN KEY ("sessions_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE
;


ALTER TABLE "measurements"

    ADD CONSTRAINT "fk_measurements_measurement_points"
    FOREIGN KEY ("measurement_points_id") 
    REFERENCES "measurement_points" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_measurements_channels"
    FOREIGN KEY ("channels_title") 
    REFERENCES "channels" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_measurements_parameters"
    FOREIGN KEY ("parameters_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;


ALTER TABLE "channels_has_parameters"

    ADD CONSTRAINT "fk_channels_has_parameters_parameters"
    FOREIGN KEY ("parameters_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;

ALTER TABLE "parameters"

    ADD CONSTRAINT "fk_parameters_units"
    FOREIGN KEY ("units_title") 
    REFERENCES "units" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;

ALTER TABLE "parameters_has_parameters"

    ADD CONSTRAINT "fk_parameters_has_parameters_parameters_parents"
    FOREIGN KEY ("parent_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_parameters_has_parameters_parameters_children"
    FOREIGN KEY ("child_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;


