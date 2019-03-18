import datetime
from haystack import indexes
# from core.models import Fiscal_Year
from core.models import Organization


class OrgIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # fiscalYear = indexes.IntegerField(model_attr='fiscal_year')

    def get_model(self):
        # return Fiscal_Year
        return Organization

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
