with sections as (
    select distinct
        section_code,
        section
    from {{ ref('stg_snowflake__imports')}}
    union
    select distinct
        section_code,
        section
    from {{ ref('stg_snowflake__exports')}}
)

select
    section_code,
    section
from sections