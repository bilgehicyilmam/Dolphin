from django.test import SimpleTestCase

class BioontologyTest(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        print("#setUpTestData: Run once to set up non-modified data for all class methods.")
        print("hiiiii")
        cls.foo = Bioontology("a", "b")
        print(cls)
        pass

    def setUp(self):
        print("#setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("#Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("#Method: test_false_is_true.")
        self.assertTrue(True)

    def test_one_plus_one_equals_two(self):
        print("#Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def test_one_plus_one_equals_two(self,cls):
        print("Method: test_filenames.")
        # bio = cls.Bioontology("owlfile.txt", "rdffile.xml")
        # self.assertEqual(bio.owl, "owlfile.txt")
