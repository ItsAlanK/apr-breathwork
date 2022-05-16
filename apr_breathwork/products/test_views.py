from django.test import TestCase
from .models import Category, Product


class TestProductsView(TestCase):
    """ Class for testing products view """

    def test_get_product_page_response(self):
        """Test response for product page and correct template used """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_category_filtering(self):
        """
        Test category filtering by URL params gives
        only 1 category and category is same as in url
        """
        category = Category.objects.create(name='Test Category')
        product_1 = Product.objects.create(
            name='Test product', price=1,
            duration=1, category=category)
        product_2 = Product.objects.create(
            name='Other product', price=1, duration=1)
        response = self.client.get(f'/products/?category={category.name}')
        self.assertEqual(response.status_code, 200)

        current_category = Category.objects.all()
        for cat in current_category:
            current_category_name = cat.name
        self.assertEqual(current_category_name, 'Test Category')

        products_on_page = response.context['products']
        self.assertEqual(products_on_page[0].name, 'Test product')

    def test_search_filtering(self):
        """
        Test search query returns filtered product page
        """
        query = 'Test'
        product_1 = Product.objects.create(
            name='Test product', price=1, duration=1)
        product_2 = Product.objects.create(
            name='Other product', price=1, duration=1)
        response = self.client.get(f'/products/?q={query}')
        products_on_page = response.context['products']
        self.assertEqual(products_on_page.count(), 1)
        self.assertEqual(products_on_page[0].name, 'Test product')


class TestProductDetailView(TestCase):
    """ Test the product detail page view """

    def test_get_product_detail_page_response(self):
        """ Test response for product detail page and correct template used """

        product_1 = Product.objects.create(
            name='Test product', price=1, duration=1)
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_detail_uses_correct_product(self):
        """
        Test that the product detail page uses the correct product
        """

        product_1 = Product.objects.create(
            name='Test product', price=1, duration=1)
        response = self.client.get(f'/products/{product_1.id}')
        product_on_page = response.context['product']
        self.assertEqual(product_on_page.name, product_1.name)
