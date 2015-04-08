# feincms_grid
An app that integrates Foundation grid with FeinCMS contenttypes.

###Installation

1. Install Foundation 5 and be sure it is working properly before getting into this package.
2. Add `'feincms\_grid'` to your `INSTALLED\_APPS` setting

###Usage

Just subclass `GridContent` when creating a content type:

    class RawTextContent(GridContent):
        content = models.TextField()

        class Meta:
            abstract = True
            
If you want to change the `render` method of the content type, be sure to call the super method to have the content wrapped with the tags:

    class MarkdownContent(GridContent):
        content = models.TextField()

        class Meta:
            abstract = True
            verbose_name = 'Markdown Text'

        def render(self, *args, **kwargs):
            t = Template(self.content)
            c = Context({})
            rendered = t.render(c)
            rendered = markdown.markdown(rendered)
            self.rendered = mark_safe(rendered)
            return super(MarkdownContent, self).render(**kwargs)
