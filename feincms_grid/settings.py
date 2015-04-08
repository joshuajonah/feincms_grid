from django.conf import settings


FEINCMS_GRID_TOTAL_COLUMNS = getattr(settings, 'FEINCMS_GRID_TOTAL_COLUMNS', 12)
FEINCMS_GRID_FIELDS = getattr(settings, 'FEINCMS_GRID_FIELDS', ('grid_columns', 'grid_push', 'grid_pull', 'grid_offset', 'grid_extra_classes'))