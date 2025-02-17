with chapters as (
    select distinct
        s.section_code,
        i.chapter_code,
        i.chapter
    from {{ ref('stg_comexstat__imports')}} as i
    join {{ ref('dim_sections')}} as s
    using (section_code)
    union
    select distinct
        s.section_code,
        e.chapter_code,
        e.chapter
    from {{ ref('stg_comexstat__exports')}} as e
    join {{ ref('dim_sections')}} as s
    using (section_code)
)

select
    section_code,
    chapter_code,
    chapter
from chapters
order by section_code, chapter_code