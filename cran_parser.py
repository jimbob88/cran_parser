import datetime
import sys
import urllib.parse
from functools import lru_cache
from pathlib import PurePosixPath
import posixpath
from typing import List, Dict, Type, Union

import bs4
import requests
from dataclasses import dataclass

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'}


@dataclass
class Package:
    name: str
    url: str


@dataclass
class PackageShortDescription(Package):
    description: str

    @staticmethod
    def create_from_tr(tr: bs4.element.Tag):
        name_td, description_td = tr.find_all('td')
        name_href = name_td.find('a')
        return PackageShortDescription(
            name=name_href.text,
            url=name_href['href'],
            description=description_td.text
        )


@dataclass
class FullPackage(PackageShortDescription):
    long_description: str
    version: str
    depends: List[Package]
    suggests: List[Package]
    publish_date: datetime.datetime
    author: str
    maintainer: str
    license: str
    needs_compilation: bool
    citation_info_url: str
    manual_url: str
    package_src_url: str
    windows_binaries_urls: Dict[str, str]
    osx_binaries_urls: Dict[str, str]
    old_sources_url: str

    @staticmethod
    def create_from_html(html: str, url: str):
        soup = bs4.BeautifulSoup(html, "lxml")
        details_table = FullPackage.get_summary_table_from_soup(soup)
        downloads_table = FullPackage.get_downloads_table(soup)
        return FullPackage(
            name=FullPackage.get_name_from_soup(soup),
            url=url,
            description=FullPackage.get_short_description_from_soup(soup),
            long_description=FullPackage.get_long_description_from_soup(soup),
            version=FullPackage.get_version_from_table(table=details_table),
            depends=FullPackage.get_depends_from_table(table=details_table),
            suggests=FullPackage.get_suggests_from_table(table=details_table),
            publish_date=FullPackage.get_date_published_from_table(table=details_table),
            author=FullPackage.get_author_from_table(table=details_table),
            maintainer=FullPackage.get_maintainer_from_table(table=details_table),
            license=FullPackage.get_license_from_table(table=details_table),
            needs_compilation=FullPackage.get_needs_compilation_from_table(table=details_table),
            citation_info_url=FullPackage.get_citation_url_from_table(table=details_table),
            manual_url=FullPackage.get_reference_manual_url_from_table(table=downloads_table),
            package_src_url=FullPackage.get_package_source_from_table(table=downloads_table),
            windows_binaries_urls=FullPackage.get_windows_binaries_from_table(table=downloads_table),
            osx_binaries_urls=FullPackage.get_osx_binaries_from_table(table=downloads_table),
            old_sources_url=FullPackage.get_old_sources_from_table(table=downloads_table)
        )

    @staticmethod
    def get_name_from_soup(soup: bs4.BeautifulSoup) -> str:
        return soup.find('h2').text.split(':')[0]

    @staticmethod
    def get_short_description_from_soup(soup: bs4.BeautifulSoup) -> str:
        return soup.find('h2').text.split(':')[1]

    @staticmethod
    def get_long_description_from_soup(soup: bs4.BeautifulSoup) -> str:
        return soup.find('p').text

    @staticmethod
    def get_summary_table_from_soup(soup: bs4.BeautifulSoup) -> bs4.element.Tag:
        return soup.find('table')

    @staticmethod
    def get_version_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='Version:').find_next_sibling('td').text

    @staticmethod
    def get_depends_from_table(table: bs4.element.Tag) -> List[Package]:
        return [Package(name=link.text, url=link['href']) for link in
                table.find('td', string='Depends:').find_next_sibling('td').find_all('a')]

    @staticmethod
    def get_suggests_from_table(table: bs4.element.Tag) -> List[Package]:
        return [Package(name=link.text, url=link['href']) for link in
                table.find('td', string='Suggests:').find_next_sibling('td').find_all('a')]

    @staticmethod
    def get_date_published_from_table(table: bs4.element.Tag) -> datetime.datetime:
        return datetime.datetime.strptime(table.find('td', string='Published:').find_next_sibling('td').text,
                                          '%Y-%m-%d')

    @staticmethod
    def get_author_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='Author:').find_next_sibling('td').text

    @staticmethod
    def get_maintainer_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='Maintainer:').find_next_sibling('td').text

    @staticmethod
    def get_license_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='License:').find_next_sibling('td').text

    @staticmethod
    def get_needs_compilation_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='NeedsCompilation:').find_next_sibling('td').text == 'yes'

    @staticmethod
    def get_citation_url_from_table(table: bs4.element.Tag) -> str:
        return table.find('td', string='Citation:').find_next_sibling('td').find('a')['href']

    @staticmethod
    def get_downloads_table(soup: bs4.BeautifulSoup) -> bs4.element.PageElement:
        return soup.find('h4', string='Downloads:').find_next('table')

    @staticmethod
    def get_reference_manual_url_from_table(table: bs4.element.Tag):
        return table.find('td', string=' Reference manual: ').find_next_sibling('td').find('a')['href']

    @staticmethod
    def get_package_source_from_table(table: bs4.element.Tag):
        return table.find('td', string=' Package source: ').find_next_sibling('td').find('a')['href']

    @staticmethod
    def get_old_sources_from_table(table: bs4.element.Tag):
        return table.find('td', string=' Old sources: ').find_next_sibling('td').find('a')['href']

    @staticmethod
    def get_windows_binaries_from_table(table: bs4.element.Tag) -> Dict[str, str]:
        return dict(zip(('r-devel', 'r-release', 'r-oldrel'),
                        [a['href'] for a in
                         table.find('td', string=' Windows binaries: ').find_next_sibling('td').find_all('a')]))

    @staticmethod
    def get_osx_binaries_from_table(table: bs4.element.Tag) -> Dict[str, str]:
        return dict(zip(('r-release', 'r-oldrel'),
                        [a['href'] for a in
                         table.find('td', string=' OS X binaries: ').find_next_sibling('td').find_all('a')]))

    def fix_urls(self, base_url: Union[str, None] = None):
        if base_url is None:
            base_url = self.url
        for idx, dependency in enumerate(self.depends):
            self.depends[idx].url = urllib.parse.urljoin(base_url, dependency.url)

        for idx, suggestion in enumerate(self.suggests):
            self.suggests[idx].url = urllib.parse.urljoin(base_url, suggestion.url)

        self.citation_info_url = urllib.parse.urljoin(base_url, self.citation_info_url)
        self.manual_url = urllib.parse.urljoin(base_url, self.manual_url)
        self.package_src_url = urllib.parse.urljoin(base_url, self.package_src_url)

        for key, url in self.windows_binaries_urls.items():
            self.windows_binaries_urls[key] = urllib.parse.urljoin(base_url, url)

        for key, url in self.osx_binaries_urls.items():
            self.osx_binaries_urls[key] = urllib.parse.urljoin(base_url, url)

        self.old_sources_url = urllib.parse.urljoin(base_url, self.old_sources_url)


class CranParser:
    def __init__(self, cran_source: str) -> None:
        """A parser for cran snapshots

        Args:
            cran_source (str): the base url for the cran
            (i.e. https://cran.microsoft.com/snapshot/2019-05-24/)
        """
        self.cran_source = cran_source

    @property
    def package_list_url(self):
        return posixpath.join(self.cran_source, 'web/packages/available_packages_by_name.html')

    @lru_cache
    def get_package_list_html(self):
        return requests.get(self.package_list_url, allow_redirects=True, headers=HEADERS).content

    def get_package_list(self):
        soup = bs4.BeautifulSoup(self.get_package_list_html(), "lxml")
        return [PackageShortDescription.create_from_tr(tr) for tr in
                soup.find('table').find_all('tr', attrs={'id': ''})]

    def get_package(self, package: Type[Package]) -> FullPackage:
        url = urllib.parse.urljoin(self.package_list_url, package.url)
        html = requests.get(url, allow_redirects=True,
                            headers=HEADERS).content
        return FullPackage.create_from_html(html, url)


def main():
    cran_parser = CranParser("https://cran.microsoft.com/snapshot/2019-05-24/")
    package_list = cran_parser.get_package_list()
    print('url: ', urllib.parse.urljoin(cran_parser.package_list_url, package_list[0].url))
    package = cran_parser.get_package(package_list[0])
    package.fix_urls()
    print(package)


if __name__ == '__main__':
    sys.exit(main())
