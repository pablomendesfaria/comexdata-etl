-- models/staging/snowflake/stg_snowflake__exports.sql
with raw_exports as (
    select * from {{ source('raw_schema', 'export_table') }}
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
    metricKG as net_weight_kg
from raw_exports