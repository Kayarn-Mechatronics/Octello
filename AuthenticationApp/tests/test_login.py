from django.test import TestCase, Client, RequestFactory
from django.test.testcases import LiveServerTestCase
from AuthenticationApp.views import LoginView
from django.contrib.auth.models import User
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLoginView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('AdminTest', 'admin@octello.rw', 'adminsecret')
        self.user.objects.create_user('StaffTest', 'staff@octello.rw', 'adminsecret')
             
    def test_basic_LoginView(self):
        request = self.factory.get('/auth/login')
        response = LoginView.login_page(request)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('AuthenticationApp/Login.html')
        
class UI_Login_process_TestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_request_LoginForm(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/auth/login'))
        
    