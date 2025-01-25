with headings as (
    select distinct
        c.chapter_code,
        i.heading_code,
        i.heading
    from {{ ref('stg_snowflake__imports')}} as i
    join {{ ref('dim_chapters')}} as c
    using (chapter_code)
    union
    select distinct
        c.chapter_code,
        e.heading_code,
        e.heading
    from {{ ref('stg_snowflake__exports')}} as e
    join {{ ref('dim_chapters')}} as c
    using (chapter_code)
)

select
    chapter_code,
    heading_code,
    heading
from headings
order by chapter_code, heading_code