from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseNotFound
from streamline.models import Url_PDF, Table_PDF, Url_HTML, Table_HTML

class TestTablesFromPdf(TestCase):

    def setUp(self) -> None:

        self.client = Client()
        self.get_tables_from_pdf_url = reverse('get_tables_from_pdf')

        self.pdf_obj = Url_PDF.objects.create(
            url = 'test.pdf',
            pdf_path = 'path/to/test.pdf'
        )

        Table_PDF.objects.create(
            pdf_id = self.pdf_obj,
            page = '6',
            file_path = 'path/to/table.csv'
        )

        return super().setUp()

    def test_get_tables_from_pdf_GET(self):

        response = self.client.get(self.get_tables_from_pdf_url, {'topic':"test.pdf", 'pages':"6"})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamline/preview_page.html')

    def test_get_tables_from_pdf_no_tables(self):

        response = self.client.get(self.get_tables_from_pdf_url, {'topic':"test.pdf", 'pages':"1"})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamline/no_tables.html')

    def test_get_tables_from_pdf_invalid_request(self):

        response = self.client.get(self.get_tables_from_pdf_url)
        
        self.assertEquals(response.status_code, 400)

    def test_get_tables_from_pdf_invalid_input(self):

        response = self.client.get(self.get_tables_from_pdf_url, {'topic':"test.pdf", 'pages':"abc"})
        
        self.assertEquals(response.status_code, 400)


class TestTablesFromHtml(TestCase):

    def setUp(self) -> None:

        self.client = Client()

        self.get_tables_from_html_url = reverse('get_tables_from_html')

        self.html_obj = Url_HTML.objects.create(
            url = 'test.com',
        )

        Table_HTML.objects.create(
            html_id = self.html_obj,
            file_path = 'path/to/table.csv'
        )

        self.html_obj_2 = Url_HTML.objects.create(
            url = 'test2.com',
        )

        return super().setUp()

    def test_get_tables_from_html_GET(self):

        response = self.client.get(self.get_tables_from_html_url, {'topic':'test.com'})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamline/preview_page.html')

    def test_get_tables_from_html_no_tables(self):

        response = self.client.get(self.get_tables_from_html_url, {'topic':'test2.com'})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamline/no_tables.html')

    def test_get_tables_from_html_invalid_request(self):

        response = self.client.get(self.get_tables_from_html_url)

        self.assertEquals(response.status_code, 400)


class TestDownloadFile(TestCase):

    def setUp(self) -> None:

        self.client = Client()

        self.pdf_obj = Url_PDF.objects.create(
            url = 'test.pdf',
            pdf_path = 'path/to/test.pdf'
        )

        self.table_obj = Table_PDF.objects.create(
            pdf_id = self.pdf_obj,
            page = '6',
            file_path = 'path/to/table.csv'
        )

        return super().setUp()

    def test_download_file_not_found(self):
        
        response = self.client.get(reverse('download_file', args=['1','html']))
        
        self.assertEquals(response.status_code, 404)

    
    def test_download_file_not_downloadable(self):

        response = self.client.get(reverse('download_file', args=[self.table_obj.id,'pdf']))
        
        self.assertEquals(response.status_code, 404)