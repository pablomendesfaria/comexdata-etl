with imports as (
    select
        c.country_id,
        s.sub_heading_code,
        i.value_dollar_fob,
        i.value_freight,
        i.value_insurance,
        i.total_value,
        i.net_weight_kg
    from {{ ref('stg_comexstat__imports')}} as i
    join {{ ref('dim_countries') }} as c
        on i.country = c.country_name
    join {{ ref('dim_subheadings') }} as s
        on i.sub_heading_code = s.sub_heading_code
)

select
    row_number() over(order by country_id, sub_heading_code) as fact_import_id,
    country_id,
    sub_heading_code,
    value_dollar_fob,
    value_freight,
    value_insurance,
    total_value,
    net_weight_kg
from imports