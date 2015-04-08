from django import template

from feincms.templatetags.feincms_tags import _render_content
from feincms_grid.settings import FEINCMS_GRID_TOTAL_COLUMNS


register = template.Library()


@register.simple_tag(takes_context=True)
def feincms_grid_render_region(context, feincms_object, region, request=None):
    """
    {% feincms_grid_render_region feincms_page "main" request %}
    """
    full_content = ''
    partial_content = ''
    use_grid = False
    combined_columns = 0
    carried_over = False

    for content in getattr(feincms_object.content, region):
    	if content.grid_columns:
    		combined_columns = combined_columns + content.grid_columns
    		rendered_content = _render_content(content, request=request, context=context)

    		if combined_columns <= FEINCMS_GRID_TOTAL_COLUMNS:
    			partial_content += rendered_content

    			if combined_columns == FEINCMS_GRID_TOTAL_COLUMNS:
	    			full_content += "<div class='row'>%s</div>" % partial_content
	    			partial_content = ''
	    			combined_columns = 0

    	else:
    		full_content += _render_content(content, request=request, context=context)

    if partial_content:
        full_content += "<div class='row'>%s</div>" % partial_content
    	
    return full_content
   