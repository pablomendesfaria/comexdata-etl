with countries as (
    select distinct
        country as country_name
    from {{ ref('stg_comexstat__imports')}}
    union
    select distinct
        country as country_name
    from {{ ref('stg_comexstat__exports')}}
)

select
    row_number() over(order by country_name collate 'en-ci-ai') as country_id,
    country_name
from countries