from django.test import SimpleTestCase
from django.urls import reverse, resolve
from streamline.views import get_tables_from_pdf, get_tables_from_html, download_file


class TestTablesFromPdf(SimpleTestCase):

    def test_get_tables_from_pdf_is_resolved(self):
        url = reverse('get_tables_from_pdf')
        self.assertEquals(resolve(url).func, get_tables_from_pdf)

    def test_get_tables_from_pdf_status_code(self):
        response = self.client.get(reverse('get_tables_from_pdf'))
        self.assertEquals(response.status_code, 200)

    def test_get_tables_from_pdf_correct_template(self):
        response = self.client.get(reverse('get_tables_from_pdf'))
        self.assertTemplateUsed(response, 'streamline/no_tables.html')

class TestTablesFromHtml(SimpleTestCase):

    def test_get_tables_from_html_is_resolved(self):
        url = reverse('get_tables_from_html')
        self.assertEquals(resolve(url).func, get_tables_from_html)

    def test_get_tables_from_html_status_code(self):
        response = self.client.get(reverse('get_tables_from_html'))
        self.assertEquals(response.status_code, 200)

    def test_get_tables_from_html_correct_template(self):
        response = self.client.get(reverse('get_tables_from_html'))
        self.assertTemplateUsed(response, 'streamline/no_tables.html')

class TestDownloadFile(SimpleTestCase):

    def test_download_file_is_resolved(self):
        url = reverse('download_file', args=['1,2,3','pdf'])
        self.assertEquals(resolve(url).func, download_file)
