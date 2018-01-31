from django.db import models
from django.test import TestCase

from .fields import CompressedListField, AutoGrowingList


class DemoModel(models.Model):
    cl = CompressedListField()
    cl_char = CompressedListField(type_code='c')
    cl_default = CompressedListField(default=[9, AutoGrowingList.EMPTY, 8])


class TestCompressedListField(TestCase):

    demo_model = DemoModel

    def test_create(self):
        obj = self.demo_model.objects.create(cl=[1, 2, 3])
        new_obj = self.demo_model.objects.get(id=obj.id)

        self.assertEqual(obj.cl, new_obj.cl)
        self.assertEqual(obj.cl, [1, 2, 3])

    def test_extend_list(self):
        obj = self.demo_model.objects.create(cl=[1, 2, 3])
        obj.cl[1000] = 4
        obj.save()
        new_obj = self.demo_model.objects.get(id=obj.id)
        self.assertEqual(new_obj.cl[1:4], [1, 2, 3])
        for i in new_obj.cl[4:-1]:
            self.assertEqual(i, AutoGrowingList.EMPTY)

        self.assertEqual(new_obj.cl[1000], 4)
        self.assertEqual(len(new_obj.cl), 1000)
