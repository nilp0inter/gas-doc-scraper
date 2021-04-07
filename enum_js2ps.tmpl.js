/*
Returns the appropiate PS data constructor from the array `a`
given a {{ function.extra['enum']['name'] }} value.
*/
export.{{ function.name }} = function (a, v) {
  switch (v) {
  {%- for c in union.constructors %}
  case a[{{ loop.index0 }}]:
    return {{ enum['properties'][loop.index0]['name'] }};
  {%- endfor %}
  default:
    throw new Error("Invalid value for {{ enum['name'] }}");
  }
};