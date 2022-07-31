import unittest

from cran_parser import CranParser


class CranParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cran_parser = CranParser("https://cran.microsoft.com/snapshot/2019-05-24/")
        return super().setUp()

    def test_init(self):
        self.assertEqual(self.cran_parser.cran_source, "https://cran.microsoft.com/snapshot/2019-05-24/")

    def test_package_list_url(self):
        self.assertEqual(self.cran_parser.package_list_url,
                         "https://cran.microsoft.com/snapshot/2019-05-24/web/packages/available_packages_by_name.html")

    def test_get_package_list(self):
        self.assertEqual(len(self.cran_parser.get_package_list()), 14272)


if __name__ == "__main__":
    unittest.main()
