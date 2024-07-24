-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
-- Modified by the team to include relationship integrity and indexes

CREATE TABLE "category" (
    "category_id" VARCHAR(10)   NOT NULL,
    "category" VARCHAR(50)   NOT NULL,
    "last_update" timestamp  DEFAULT Localtimestamp NOT NULL,
    CONSTRAINT "pk_category" PRIMARY KEY (
        "category_id"
     )
);

CREATE TABLE "subcategory" (
    "subcategory_id" VARCHAR(12)   NOT NULL,
    "subcategory" VARCHAR(50)   NOT NULL,
    "last_update" timestamp  DEFAULT Localtimestamp NOT NULL,
    CONSTRAINT "pk_subcategory" PRIMARY KEY (
        "subcategory_id"
     )
);

CREATE TABLE "campaign" (
    "funding_id" int   NOT NULL,
    "contact_id" int   NOT NULL,
    "company_name" VARCHAR(50)   NOT NULL,
    "description" VARCHAR(75)   NOT NULL,
    "goal" decimal   NOT NULL,
    "pledged" decimal   NOT NULL,
    "outcome" VARCHAR(10)   NOT NULL,
    "backers_count" int   NOT NULL,
    "country" VARCHAR(2)   NOT NULL,
    "currency" VARCHAR(3)   NOT NULL,
    "launched_date" timestamp   NOT NULL,
    "end_date" timestamp   NOT NULL,
    "staff_pick" boolean   NOT NULL,
    "spotlight" boolean   NOT NULL,
    "category_id" VARCHAR(10)   NOT NULL,
    "subcategory_id" VARCHAR(12)   NOT NULL,
    "last_update" timestamp  DEFAULT Localtimestamp NOT NULL,
    CONSTRAINT "pk_campaign" PRIMARY KEY (
        "funding_id"
     )
);

CREATE TABLE "contact" (
    "contact_id" int   NOT NULL,
    "first_name" VARCHAR(30)   NOT NULL,
    "last_name" VARCHAR(30)   NOT NULL,
    "email" VARCHAR(50)   NOT NULL,
    "last_update" timestamp  DEFAULT Localtimestamp NOT NULL,
    CONSTRAINT "pk_contact" PRIMARY KEY (
        "contact_id"
     )
);

ALTER TABLE "campaign" ADD CONSTRAINT "fk_campaign_contact_id" FOREIGN KEY("contact_id")
REFERENCES "contact" ("contact_id");

ALTER TABLE "campaign" ADD CONSTRAINT "fk_campaign_category_id" FOREIGN KEY("category_id")
REFERENCES "category" ("category_id");

ALTER TABLE "campaign" ADD CONSTRAINT "fk_campaign_subcategory_id" FOREIGN KEY("subcategory_id")
REFERENCES "subcategory" ("subcategory_id");

-- Indexes for Primary Keys
CREATE UNIQUE INDEX idx_cat_id
    ON public.category (category_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX idx_subcat_id
    ON public.subcategory (subcategory_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX idx_cont_id
    ON public.contact (contact_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX idx_camp_id
    ON public.campaign (funding_id)
    TABLESPACE pg_default;

-- Indexes for foreign keys and where clauses
CREATE INDEX isx_camp_outcome_id
    ON public.campaign (outcome ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.campaign
    CLUSTER ON isx_camp_outcome_id;

CREATE INDEX isx_camp_country_id
    ON public.campaign (country ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.campaign
    CLUSTER ON isx_camp_country_id;

CREATE INDEX isx_camp_staff_id
    ON public.campaign (staff_pick ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.campaign
    CLUSTER ON isx_camp_staff_id;

CREATE INDEX isx_camp_spotlight_id
    ON public.campaign (spotlight ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.campaign
    CLUSTER ON isx_camp_spotlight_id;

-- Verification of the table creation, is on a separate file called "select_sql.sql"