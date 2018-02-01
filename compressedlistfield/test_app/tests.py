from django.test import TestCase

from compressedlistfield import AutoGrowingList
from .models import DemoModel


class TestCompressedListField(TestCase):

    demo_model = DemoModel

    def test_create(self):
        obj = self.demo_model.objects.create(cl=AutoGrowingList([1, 2, 3]))
        new_obj = self.demo_model.objects.get(id=obj.id)

        self.assertEqual(obj.cl, new_obj.cl)
        self.assertEqual(obj.cl, [1, 2, 3])

    def test_extend_list(self):
        obj = self.demo_model.objects.create(cl=AutoGrowingList([1, 2, 3]))
        obj.cl[1000] = 4
        obj.save()
        new_obj = self.demo_model.objects.get(id=obj.id)
        self.assertEqual(new_obj.cl[1], 1)
        self.assertEqual(new_obj.cl[2], 2)
        self.assertEqual(new_obj.cl[3], 3)
        for i in new_obj.cl[4:-1]:
            self.assertEqual(i, AutoGrowingList.EMPTY)

        self.assertEqual(new_obj.cl[1000], 4)
        self.assertEqual(len(new_obj.cl), 1000)
