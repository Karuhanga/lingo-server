from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from lingo_server.models import Word, Language

FIELDS = ('word', 'language')


class WordResource(resources.ModelResource):
    class Meta:
        model = Word
        fields = FIELDS
        export_order = FIELDS
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('word',)

    language = Field(attribute='language', column_name='language', widget=ForeignKeyWidget(Language, 'name'))
