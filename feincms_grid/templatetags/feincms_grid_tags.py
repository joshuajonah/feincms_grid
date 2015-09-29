from django import template

from feincms.templatetags.feincms_tags import _render_content
from feincms_grid.settings import FEINCMS_GRID_TOTAL_COLUMNS


register = template.Library()


class NoGridValuesException(Exception):
    pass


class GridBuilder(object):
    items = []
    row_columns = 0
    current_row = []
    return_string = ''

    def __init__(self, request, context={}):
        self.request = request
        self.context = context
        self.row_columns = 0
        self.items = []
        self.current_row = []
        self.return_string = ''

    def add(self, item):
        self.items.append(item)

    def clear_queue(self, orphan=None):
        self.row_columns = 0
        self.current_row = []
        if orphan:
            self.current_row.append(orphan)

    def render_row(self, content, wrap=True):
        if type(content) == list:
            content = ''.join(content)
        if wrap:
            self.return_string += "<div class='row'>%s</div>" % content
        else:
            self.return_string += content
        
    def render(self):
        for item in self.items:
            rendered = _render_content(item, request=self.request, context=self.context)
            
            # In case you try to render a contenttype that isn't a subclass of GridContent.
            try:
                if item.grid_columns:
                    # Add current column to the total combined row columns.
                    item_columns = item.grid_columns
                    if item.grid_offset:
                        item_columns += item.grid_offset

                    # Can't add, starting a new row with the item.
                    if self.row_columns + item_columns > FEINCMS_GRID_TOTAL_COLUMNS:
                        self.render_row(self.current_row)
                        self.clear_queue(rendered)

                    # Add it to the row.
                    else:
                        self.row_columns += item_columns
                        self.current_row.append(rendered)

                        # If this row is full, start a new one.
                        if self.row_columns == FEINCMS_GRID_TOTAL_COLUMNS:
                            self.render_row(self.current_row)
                            self.clear_queue()

                # No defined grid_columns
                else:
                    raise NoGridValuesException

            # Do it the old fashined way.
            except (AttributeError, NoGridValuesException):
                self.render_row(rendered, wrap=False)
                self.clear_queue()

        # Make sure to render any left overs.
        if self.current_row:
            self.render_row(self.current_row)

        # Clear out this object.
        self.items = []
        self.clear_queue()

        return self.return_string


@register.simple_tag(takes_context=True)
def feincms_grid_render_region(context, feincms_object, region, request=None):
    """
    {% feincms_grid_render_region feincms_page "main" request %}
    """

    grid = GridBuilder(request, context)

    for content in getattr(feincms_object.content, region):
        grid.add(content)

    return grid.render()
