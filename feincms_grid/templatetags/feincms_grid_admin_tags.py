from django import template

from feincms_grid.settings import FEINCMS_GRID_FIELDS


register = template.Library()


@register.filter
def post_process_fieldsets(fieldset, remove=None, keep=None):
    """
    Removes a few fields from FeinCMS admin inlines, those being
    ``id``, ``DELETE`` and ``ORDER`` currently.

    Additionally, it ensures that dynamically added fields (i.e.
    ``ApplicationContent``'s ``admin_fields`` option) are shown.
    """
    # abort if fieldset is customized
    if fieldset.model_admin.fieldsets:
        return fieldset

    fields_to_include = set(fieldset.form.fields.keys())
    for f in ('id', 'DELETE', 'ORDER'):
        fields_to_include.discard(f)

    if remove:
        for f in FEINCMS_GRID_FIELDS:
            fields_to_include.discard(f.strip())

    if keep:
        for f in list(fields_to_include):
            if f not in keep:
                fields_to_include.discard(f)

    def _filter_recursive(fields):
        ret = []
        for f in fields:
            if isinstance(f, (list, tuple)):
                # Several fields on one line
                sub = _filter_recursive(f)
                # Only add if there's at least one field left
                if sub:
                    ret.append(sub)
            elif f in fields_to_include:
                ret.append(f)
                fields_to_include.discard(f)
        return ret

    new_fields = _filter_recursive(fieldset.fields)
    # Add all other fields (ApplicationContent's admin_fields) to
    # the end of the fieldset
    for f in fields_to_include:
        new_fields.append(f)

    fieldset.fields = new_fields
    return fieldset


@register.filter
def only_grid_fields(form):
    new_fieldsets = []
    for fieldset in form:
        fieldset = post_process_fieldsets(fieldset, keep=FEINCMS_GRID_FIELDS)
        new_fieldsets.append(fieldset.fields)
    form.fieldsets = [(None, {'fields': new_fieldsets})]
    if not new_fieldsets[0]:
        return None
    return form
