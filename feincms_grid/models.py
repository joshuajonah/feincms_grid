from django.db import models

from settings import FEINCMS_GRID_TOTAL_COLUMNS


class GridContent(models.Model):
    grid_columns = models.PositiveSmallIntegerField('Columns', blank=True, null=True, help_text='How many columns of the total (%s) this content will span.' % FEINCMS_GRID_TOTAL_COLUMNS)
    grid_offset = models.PositiveSmallIntegerField('Offset', blank=True, null=True, help_text='Offset to the right this many columns.')
    grid_push = models.PositiveSmallIntegerField('Push', blank=True, null=True, help_text='Source ordering - push this content this many columns to the right.')
    grid_pull = models.PositiveSmallIntegerField('Pull', blank=True, null=True, help_text='Source ordering - pull this content this many columns to the left.')
    grid_extra_classes = models.CharField('Extra classes', max_length=255, blank=True, help_text='Manual class definitions, e.g.: centered, large-X, small-X, etc.')

    class Meta:
        abstract = True

    def render(self, **kwargs):
        """
        Render implimentation that attempts to add CSS grid classes to the final output.
        """
        classes = []
        if self.grid_columns:
            classes.append('large-%s columns' % self.grid_columns)
        if self.grid_offset:
            classes.append('large-offset-%s' % self.grid_offset)
        if self.grid_push:
            classes.append('large-push-%s' % self.grid_push)
        if self.grid_pull:
            classes.append('large-pull-%s' % self.grid_pull)
        if self.grid_extra_classes:
            for c in self.grid_extra_classes.split(' '):
                classes.append(c)

        return "<div class='%s'>%s</div>" % (' '.join(classes), self.content)