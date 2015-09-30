# FeinCMS Grid
An app that integrates Foundation grid with FeinCMS contenttypes. Currently only for Foundation, but other frameworks grid syntax is so similar, I'll likely expand this to handle multiple grid systems later.

###Installation

1. Install Foundation 5 and be sure it is working properly before getting into this package.
2. Run `pip install feincms-grid`.
3. Add `'feincms_grid'` to your `INSTALLED_APPS` setting.
4. Add `FEINCMS_GRID_TOTAL_COLUMNS` to your settings if you want to override the total column amount (default is 12).

###Configuration

#####Content types

Just subclass `GridContent` when creating a content type:

    from feincms_grid.models import GridContent

    class RawTextContent(GridContent):
        content = models.TextField()

        class Meta:
            abstract = True
            
If you want to change the `render` method of the content type, be sure to call the `super` method to have the content wrapped with the tags:

    from feincms_grid.models import GridContent

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
            self.content = mark_safe(rendered)
            return super(MarkdownContent, self).render(*args, **kwargs)

#####Templates

Use the `feincms_grid_render_region` tag to render regions in your templates.

    {% extends 'base.html' %}
	{% load feincms_page_tags feincms_grid_tags %}

	{% block content %}
		{% feincms_grid_render_region feincms_page "main" request %}
	{% endblock %}

###Usage

Any content types which are subclasses of `GridContent` will have an extra dropdown at the top of them:

![usage preview](https://github.com/joshuajonah/feincms_grid/blob/master/feincms_grid.png)
