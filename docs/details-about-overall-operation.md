# Details about overall operation

> [!NOTE]  
> This is only the **default behaviour** as you can tune this with your own plugins!

Let's imagine the following directory structure:

```
/foo/
/foo/README.md.template
/foo/bar/baz.py.template
/foo/bar/another.file
```

And execute `jinja-tree /foo` with the default configuration.

We get:

```
/foo/
/foo/README.md.template
/foo/README.md <= NEW FILE FROM README.md.template jinja2 processing
/foo/bar/baz.py.template
/foo/bar/baz.py <= NEW FILE FROM baz.py.template jinja2 processing 
/foo/bar/another.file
```

Go back to [main README](../README.md) file.
