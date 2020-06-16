### Default Zettel ID Format (`default_zettel_id_format`)

> Default value: `%Y%m%d%H%M`

This option defines the format used for the generated Zettel ID and the `{zettel_id}` placeholder in your templates. Since there is the potential of creating duplicate Zettel IDs with this workflow, you may wish to customise this. For example, I use the following format for my Zettel IDs:  `%y%m%d%H%M%S` (i.e. yymmddHHMMSS).

Please refer to the [Python strftime reference](https://strftime.org/) for the available datetime variables.
