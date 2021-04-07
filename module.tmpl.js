/*
This module has been generated automatically by gas-doc-scrapper
DO NOT MODIFY
*/

{% for e in module.declarations %}
{{ e.render_js_part(api=api, module=module) }}
{% endfor %}