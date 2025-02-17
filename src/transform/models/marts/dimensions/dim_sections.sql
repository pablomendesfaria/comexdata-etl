with sections as (
    select distinct
        section_code,
        section
    from {{ ref('stg_comexstat__imports')}}
    union
    select distinct
        section_code,
        section
    from {{ ref('stg_comexstat__exports')}}
)

select
    section_code,
    section
from sections