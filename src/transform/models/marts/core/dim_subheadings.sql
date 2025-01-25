with subheadings as (
    select distinct
        h.heading_code,
        i.sub_heading_code,
        i.sub_heading
    from {{ ref('stg_snowflake__imports')}} as i
    join {{ ref('dim_headings')}} as h
    using (heading_code)
    union
    select distinct
        h.heading_code,
        e.sub_heading_code,
        e.sub_heading
    from {{ ref('stg_snowflake__exports')}} as e
    join {{ ref('dim_headings')}} as h
    using (heading_code)
)

select
    heading_code,
    sub_heading_code,
    sub_heading
from subheadings
order by heading_code, sub_heading_code