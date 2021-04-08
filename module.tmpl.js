/*
This module has been generated automatically by gas-doc-scrapper
with data obtained from:

{{ enum['url'] }}

                        ** DO NOT MODIFY **

*/

{%- for e in module.declarations -%}
{{ e.render_js_part(api=api, module=module) }}
{% endfor %}