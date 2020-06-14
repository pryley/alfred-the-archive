## Exact Match (`exact_match`)

This option determines if the search should match the exact search term (`True`) or the string (`False`). 

**Note:** When exact match is set to `True` it is possible to enhance the search term with wildcards

When set to `True`, searching for `Books` will match `Books` but not `Bookstore`. However, `Books*` will match both `Books` and `Bookstore`. 

When set to `False`, searching for `Books` will match `Books` as well as `Bookstore`
