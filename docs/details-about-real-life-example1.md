# Real life example1

This is a real-life example of how we use `jinja-tree` in this repository to 
get `jinja-tree --help` output automatically added (and updated) in the main README.

## How it works

**Most important**: we maintain the `README.md` file of this repository under the file `README.md.template`.

So, the real `README.md` file *(the one that GitGub displays by default when someone goes to your repository)* is generated from `README.md.template` using `jinja-tree` (or with `make doc` command). 

Now, to include and maintain automatically the `jinja-tree --help` output in the `README.md` file, we use the following `README.md.template` file:

````markdown
# jinja-tree

## What is it?

[...]

## CLI documentation

Here is the CLI documentation:

```
{{ "jinja-tree --help" | shell() }}
```
````

Note the usage of the `shell` filter (Jinja2 extension embedded in `jinja-tree`) to execute any command and include its output in the rendered file.

## Bonus

To avoid someone modifying the `README.md` file directly (instead of the `README.md.template` file), you can add:

```
{{JINJA_TREE_STYLE1_GENERATED_COMMENT}}
```

at the top of your `README.md.template`.

It will be rendered as a markdown comment in the `README.md` file with a warning message you can customize.

For example, this template var is automatically rendered as:

```
<!-- *** GENERATED FILE - DO NOT EDIT *** -->
<!-- To modify this file, edit README.md.template and launch 'make doc' -->
```

*(with our configuration)*


Go back to [main README](../README.md) file.