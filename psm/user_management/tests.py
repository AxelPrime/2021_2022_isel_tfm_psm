# from django.test import TestCase
#
# # Create your tests here.
#
#
# class UserTests(TestCase):
#     def test_login_page(self):
#         response = self.client.get('/login/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, '')
#
#     def test_login_user(self):
#         request_data = {
#             'email': "admin@mail.com",
#             "password": "lePassword123"
#         }
#         response = self.client.post("/api/users/login/", data=request_data, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#
#     def test_logout(self):
#         request_data = {
#             'email': "admin@mail.com",
#             "password": "lePassword123"
#         }
#         self.client.post("/api/users/login/", data=request_data, content_type='application/json', follow=True)
#         response = self.client.post("/api/users/logout/", content_type='application/json', follow=True)
#         self.assertEqual(response.status_code, 200)