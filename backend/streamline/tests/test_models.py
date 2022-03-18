from django.conf import settings
from django.test import TestCase
from streamline.models import Table_HTML, Table_PDF, Url_HTML, Url_PDF


class TestUrlPdf(TestCase):
    def test_url_pdf_creation(self):
        pdf = Url_PDF.objects.create(url="test.pdf", pdf_path="path/to/test.pdf")

        self.assertIsNotNone(pdf)

    def test_url_pdf_deletion_if_max_entries_is_reached(self):

        first_pdf = Url_PDF.objects.create(url="test.pdf", pdf_path="path/to/test.pdf")

        for i in range(settings.MAX_ENTRIES):
            Url_PDF.objects.create(
                url="test_{i}.pdf".format(i=i), pdf_path="path/to/test.pdf"
            )

        result = Url_PDF.objects.filter(id=first_pdf.id).first()

        self.assertIsNone(result)


class TestUrlHtml(TestCase):
    def test_url_html_creation(self):
        html = Url_HTML.objects.create(url="test.com")

        self.assertIsNotNone(html)

    def test_url_html_deletion_if_max_entries_is_reached(self):

        first_html = Url_HTML.objects.create(
            url="test.com",
        )

        for i in range(settings.MAX_ENTRIES):
            Url_HTML.objects.create(
                url="test_{i}.com".format(i=i),
            )

        result = Url_HTML.objects.filter(id=first_html.id).first()

        self.assertIsNone(result)


class TestTablePdf(TestCase):
    def setUp(self) -> None:

        self.pdf = Url_PDF.objects.create(url="test.pdf", pdf_path="path/to/test.pdf")

        return super().setUp()

    def test_table_pdf_creation(self):

        table = Table_PDF.objects.create(
            pdf_id=self.pdf, page=5, file_path="path/to/table.csv"
        )

        self.assertIsNotNone(table)

    def test_table_pdf_on_deletion_cascade(self):

        table = Table_PDF.objects.create(
            pdf_id=self.pdf, page=5, file_path="path/to/table.csv"
        )

        self.assertIsNotNone(table)

        Url_PDF.objects.filter(id=self.pdf.id).first().delete()

        table = Table_PDF.objects.filter(id=table.id).first()

        self.assertIsNone(table)


class TestTableHtml(TestCase):
    def setUp(self) -> None:

        self.html = Url_HTML.objects.create(url="test.com")

        return super().setUp()

    def test_table_html_creation(self):

        table = Table_HTML.objects.create(
            html_id=self.html, file_path="path/to/table.csv"
        )

        self.assertIsNotNone(table)

    def test_table_html_on_deletion_cascade(self):

        table = Table_HTML.objects.create(
            html_id=self.html, file_path="path/to/table.csv"
        )

        self.assertIsNotNone(table)

        Url_HTML.objects.filter(id=self.html.id).first().delete()

        table = Table_HTML.objects.filter(id=table.id).first()

        self.assertIsNone(table)
