{% if parents|length > 0 %}
/*
Returns the appropiate PS data constructor from the array `a`
given a {{ function.extra['enum']['name'] }} value.
*/
export.{{ function.name }} = function (a, v) {
  switch (v) {
  {%- for c in union.constructors %}
  case {{ parents[0]['name'] }}.{{ enum['name'] }}.{{ enum['properties'][loop.index0]['name'] }}:
    return a[{{ loop.index0 }}];  // {{ c }} :: {{ union.name }}
  {%- endfor %}
  default:
    throw new Error("Invalid value for {{ enum['name'] }}");
  }
};
{% else %}
/*
Returns the appropiate PS data constructor from the array `a`
given a {{ function.extra['enum']['name'] }} value.

Also it is neccesary to provide de base object where
{{ enum['name'] }} can be found.

*/
export.{{ function.name }} = function (o, a, v) {
  switch (v) {
  {%- for c in union.constructors %}
  case a[{{ loop.index0 }}]:  // {{ c }} :: {{ union.name }}
    return o.{{ enum['properties'][loop.index0]['name'] }};
  {%- endfor %}
  default:
    throw new Error("Invalid value for {{ enum['name'] }}");
  }
};
{% endif %}