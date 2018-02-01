from django.db import models

from compressedlistfield.fields import CompressedListField, AutoGrowingList


class DemoModel(models.Model):
    cl = CompressedListField()
    cl_char = CompressedListField(type_code='c')
    cl_default = CompressedListField(default=[9, AutoGrowingList.EMPTY, 8])
