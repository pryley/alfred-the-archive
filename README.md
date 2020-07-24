# Alfred Workflow for The Archive

This is an comprehensive workflow for The Archive that helps you work with your notes more efficiently.

## Table of Contents

- [Installation](#installation)
- [Searching Notes](#searching-notes)
- [Searching Tasks](#searching-tasks)
- [Searching Tags](#searching-tags)
- [Random Notes](#random-notes)
- [Creating Notes](#creating-notes)
- [Templates](#templates)
- [Importing URLs](#importing-urls)
- [Importing Images](#importing-images)
- [Text Manipulation](#text-manipulation)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Changelog](#changelog)
- [Credits](credits)

## Installation

1. Download [the latest release](https://github.com/pryley/alfred-the-archive/releases/latest/download/The.Archive.alfredworkflow)
2. Double-click the downloaded workflow to install in Alfred.
3. Install [Glance](https://apps.apple.com/us/app/glance-quick-look-plugin/id1513574319) from the App Store (optional, this allows you to Quickview markdown files)
4. Install [pandoc](https://pandoc.org/) with [Homebrew](https://brew.sh/) (optional, this allows you to import a webpage into a note)
    ```bash
    brew install pandoc
    ```

## Searching Notes

To search your notes, type `ar` along with a space, then enter your search query. 

![](screenshots/ar.png)

> **Tip:** You may change the [exact_match](#exact-match-exact_match) and [search_content](#search-content-search_content) options to configure how the workflow searches The Archive.

### Modifier keys

There are three modifier keys that you can use with the search results:

1. **⇧ Shift:** Pressing this key will use Quicklook to preview the selected note.

   > **Note:** To view markdown files with Quicklook, you may need to [install Glance](#installation).

2. **⌥ Option:** Holding this key down as you press Enter will paste a wiki link of the selected note into the frontmost application (i.e. `[[title of the selected note]]`).

3. **⌘ Command:** Holding this key down as you press Enter will display the following "Actions" menu:

   ![](screenshots/ar_action_menu.png)

## Searching Tasks

Tasks are Github-flavoured checkboxes:

```markdown
- [x] This is a completed task
- [ ] This is an uncompleted task
```

To search for tasks in your notes, type `artask` along with a space, then enter your search query. Pressing Enter on a task will toggle its status (checked/unchecked).

![](screenshots/artask.png)

### Modifier keys

There are two modifier keys that you can use with tasks:

1. **⌥ Option:** Holding this key down as you press Enter will open the note containing the task in the default editor.

2. **⌘ Command:** Holding this key down as you press Enter will open the note containing the task in The Archive.

## Searching Tags

To search the tags in your notes, type `artag` along with a space, then enter your search query. Pressing Enter on a tag will match all notes that contain the tag in The Archive.

![](screenshots/artag.png)

> **Note:** Due to a limitation of the external link URL scheme that The Archive uses, it is not possible to pass the `#` symbol along with the tag name to The Archive.

### Modifier keys

There is one modifier key that you can use with tags:

1. **⌘ Command:** Holding this key down as you press Enter will paste the selected tag into the frontmost application.

## Random Notes

To display a random note in The Archive, type `arrandom` and press Enter.

![](screenshots/arrandom.png)

## Creating Notes

To create a note, type `arnew` along with a space, then enter the title of the note and optionally some tags. If you use a template, the title you enter will fill the `{title}` placeholder, and any tags you enter will fill the `{tags}` placeholder.

![](screenshots/arnew.png)

### Modifier keys

There are two modifier keys (and one modifier key combo) that you can use when creating a note without a template:

1. **⌥ Option:** Holding this key down as you press Enter will paste the current clipboard contents into the note below the tags.

2. **⌘ Command:** Holding this key down as you press Enter will either remove or add the Zettel ID to the note depending on whether or not you have enabled the "Use ID for empty file names" option in The Archive preferences.

3. **⌘ Command + ⌥ Option:** Holding these two keys down as you press Enter will both paste the current clipboard contents into the note below the tags, and remove or add the Zettel ID to the note depending on whether or not you have enabled the "Use ID for empty file names" option in The Archive preferences.

## Templates

Templates are simply notes in The Archive that are tagged with `#template`. To create a note using a template, type `arnew` along with a space, enter the title of the note and optionally some tags, and then select the template that you wish to use.

![](screenshots/arnew_templates.png)

> **Note:** The template tag must be used within the first 10 lines of the note else it will not be recognised as a template.

> **Tip:** You may change the [template_tag](#template-tag-template_tag) option to set a custom template tag.

You may use the following placeholders in your templates:

- `{content}` This is the content of the clipboard if you have selected to paste it.
- `{date}` This is the formatted today date.
- `{tags}` These are the tags if provided.
- `{title}` This is the title of your note.
- `{zettel_id}` This is the Zettel ID of the note if used.

Here is an example Template:

```markdown
---
Title: [[{zettel_id}]] {title}
Index: [[200615130000]] Application support
Keywords: #support {tags} #template
---

{content}
```

> **Tip:** You may change the [use_zettel_id_in_title](#use-zettel-id-in-title-use_zettel_id_in_title) option to configure whether or not the `{title}` placeholder contains the Zettel ID. To change the datetime format used in the `{date}` placeholder, change the [default_date_format](#default-date-format-default_date_format) option.

### Modifier keys

There are three modifier keys (and one modifier key combo) that you can use with the search results:

1. **⇧ Shift:** Pressing this key will use Quicklook to preview the selected template.

   > **Note:** To view markdown files with Quicklook, you may need to [install Glance](#installation).

2. **⌥ Option:** Holding this key down as you press Enter will paste the current clipboard contents into the template's `{content}` placeholder.

3. **⌘ Command:** Holding this key down as you press Enter will either remove or add the Zettel ID to the note depending on whether or not you have enabled the "Use ID for empty file names" option in The Archive preferences.
4. **⌘ Command + ⌥ Option:** Holding these two keys down as you press Enter will both paste the current clipboard contents into the template's `{content}` placeholder, and remove or add the Zettel ID to the note depending on whether or not you have enabled the "Use ID for empty file names" option in The Archive preferences.

## Importing URLs

To import the page content of a webpage into a note, type `arurl` along with a space and enter a valid URL beginning with `http(s)`.

![](screenshots/arurl.png)

> **Note:** This action requires that you have [pandoc installed on your mac](#installation). Pandoc is a universal document converter and is used to convert the HTML of a webpage to Github-flavoured markdown. If you do not have pandoc installed, then only the URL will be copied into the note.

## Importing Images

The workflow provides an **Add image to The Archive** File Action which allows you to import a JPG or PNG image into the Resources Subfolder of your notes directory.

![](screenshots/image_file_action.png)

To use the File Action:

1. First you need to set your prefered "Selection Hotkey" for Actions. You can find this option on the `Features > Actions > General` tab in the Alfred Preferences.
2. Select the image in Finder and press the "Selection Hotkey" that you set in Alfred Preferences.
3. Type `add` and select the "Add image to The Archive" file action.
4. Paste the generated markdown link of the image into your note. 

## Text Manipulation

The workflow provides several hotkeys which allow you to perform basic text manipulation such as changing the heading levels of a line in your note, or marking multiple lines of text as a fenced code block using backticks. A hotkey is simply a combination of keys that you press together in order to perform an action. These hotkeys are specific to The Archive and will only work if The Archive is the front most application and in focus.

To use these hotkeys, click on the line in your note that you wish to change and then press the hotkey.

> **Note:** These hotkeys use the **⇧⌘L** keyboard shortcut that is provided by The Archive to select the current line of text. If you have mapped this keyboard shortcut to something else, then these hotkeys will not work.

### Hotkeys

- **⌘ + 1**: Pressing this hotkey will change the line to a Heading 1
- **⌘ + 2**: Pressing this hotkey will change the line to a Heading 2
- **⌘ + 3**: Pressing this hotkey will change the line to a Heading 3
- **⌘ + 4**: Pressing this hotkey will change the line to a Heading 4
- **⌘ + 5**: Pressing this hotkey will change the line to a Heading 5
- **⌘ + 6**: Pressing this hotkey will change the line to a Heading 6
- **⌘ + `**: Pressing this hotkey will wrap the selected lines of text in backticks as a fenced code block

## Configuration

To change the configuration of the workflow, type `arconfig` in Alfred. You can also view the help file for each highlighted option with Quicklook by pressing the **⇧ Shift** key.

![](screenshots/arconfig.png)

> **Note:** To view markdown files with Quicklook, you may need to [install Glance](#installation).

### Default Date Format (`default_date_format`)

> Default value: `%A, %d %B, %Y at %H:%M`

This option defines the datetime format used for the `{date}` placeholder in your templates. 

Please refer to the [Python strftime reference](https://strftime.org/) for the available datetime variables.

### Default Zettel ID Format (`default_zettel_id_format`)

> Default value: `%Y%m%d%H%M`

This option defines the datetime format used for the generated Zettel ID and the `{zettel_id}` placeholder in your templates.

Please refer to the [Python strftime reference](https://strftime.org/) for the available datetime variables.

### Exact Match (`exact_match`)

> Default value: `False`

This option defines if the search should match the exact search term (`True`) or the string (`False`). When the value is set to `True` it is possible to enhance the search term with wildcards. 

When set to `True`, searching for `Books` will match `Books` but not `Bookstore`. However, `Books*` will match both `Books` and `Bookstore`. 

When set to `False`, searching for `Books` will match `Books` as well as `Bookstore`.

### Prefer Filename to Title (`prefer_filename_to_title`)

> Default value: `True`

This option defines which value is used when matching a search result in The Archive (i.e. `thearchive://match/{value}`).

When set to `True`, the note filename will be used.

When set to `False`, the note title (if entered as `# Note Title`) will be used if it exists instead of the filename.

### Prefer Zettel ID Links (`prefer_zettel_id_links`)

> Default value: `False`

When set to `True`, the Zettel ID (if one exists) will be used as the link title in markdown and wiki links (i.e. `[[202006131200]]`). 

When set to `False`, the full note title will be used in markdown and wiki links (i.e. `[[202006131200 The Note Title]]`). 

### Search Content (`search_content`)

> Default value: `False`

When set to `True`, both the filenames and note contents will be searched.

When set to `False`, only the filenames will be searched. 

### Search YAML Tags Only (`search_yaml_tags_only`)

> Default value: `False`

When set to `True`, tags will only be searched for in the YAML front matter.

When set to `False`, tags will be searched for in the entire note. 

### Template Tag (`template_tag`)

> Default value: `#template`

The template tag defines which notes are used as templates. Add the template tag somewhere in the first 10 lines of a note and it will be recognized as an available template when you create a note.

### The Archive Bundle ID (`the_archive_bundle_id`)

> Default value: `de.zettelkasten.TheArchive`

A bundle ID (or bundle identifier) uniquely identifies an application in Apple's ecosystem. This means that no two applications can have the same bundle identifier. 

This workflow uses the bundle identifier together with [the_archive_team_id](#the-archive-team-id-the_archive_team_id) to get the saved preferences of The Archive.

This value should never need changing.

### The Archive Team ID (`the_archive_team_id`)

> Default value: `FRMDA3XRGC`

A team ID (or team identifier) is generated by Apple and uniquely identifies the developer of an application in Apple's ecosystem.

This workflow uses the team identifier together with [the_archive_bundle_id](#the-archive-bundle-id-the_archive_bundle_id) to get the saved preferences of The Archive.

This value should never need changing.

### Use Zettel ID in Title (`use_zettel_id_in_title`)

> Default value: `False`

When set to `True`, the Zettel ID will be included in the `{title}` placeholder of your templates. 

When set to `False`, the Zettel ID will not be included in the `{title}` placeholder of your templates.

## Documentation

You may view this README.md file at any time by typing `arhelp` in Alfred.

![](screenshots/arhelp.png)

## Changelog

See: [Releases](https://github.com/pryley/alfred-the-archive/releases)

## Credits

This workflow was created by [Paul Ryley](https://github.com/pryley/). Special thanks to [Acidham](https://github.com/Acidham) author of [Alfred Markdown Notes](https://github.com/Acidham/alfred-markdown-notes) which was the inspiration for this workflow.

![](screenshots/ardonate.png)

## License

The MIT License (MIT).
