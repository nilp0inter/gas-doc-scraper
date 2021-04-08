{% if parents|length > 0 -%}
export.{{function.name}} = {{ parents[0]['name'] }}.{{ enum['name'] }}.{{ property['name'] }};
{%- else -%}
export.{{function.name}} = function (o) {
    return o.{{ enum['name'] }}.{{ property['name'] }};
}
{%- endif %}