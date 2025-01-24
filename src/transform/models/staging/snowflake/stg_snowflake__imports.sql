-- models/staging/snowflake/stg_snowflake__imports.sql
with raw_imports as (
    select * from {{ source('raw_schema', 'import_table') }}
)

select
    coNcmSecrom as section_code,
    section,
    chapterCode as chapter_code,
    chapter,
    headingCode as heading_code,
    heading,
    subHeadingCode as sub_heading_code,
    subHeading as sub_heading,
    country,
    metricFOB as value_dollar_fob,
    metricFreight as value_freight,
    metricInsurance as value_insurance,
    metricCIF as total_value,
    metricKG as net_weight_kg
from raw_imports