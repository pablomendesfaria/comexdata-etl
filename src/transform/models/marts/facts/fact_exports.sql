with exports as (
    select
        c.country_id,
        s.sub_heading_code,
        e.value_dollar_fob,
        e.net_weight_kg
    from {{ ref('stg_comexstat__exports')}} as e
    join {{ ref('dim_countries') }} as c
        on e.country = c.country_name
    join {{ ref('dim_subheadings') }} as s
        on e.sub_heading_code = s.sub_heading_code
)

select
    row_number() over(order by country_id, sub_heading_code) as fact_export_id,
    country_id,
    sub_heading_code,
    value_dollar_fob,
    net_weight_kg
from exports