from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Project

class ProjectAPITests(APITestCase):
    """
    Tests for the Project API.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        This method is called once and creates a project instance
        that will be used in the tests.
        """
        cls.project = Project.objects.create(
            title="Test Project",
            description="A description for the test project.",
            technologies="Python, Django"
        )
        cls.list_url = reverse('project-list') # Assumes basename='project' in urls.py

    def test_list_projects(self):
        """
        Ensure we can retrieve a list of projects.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Check that there is one project

        # Check that the data for our project is in the response
        project_data = response.data[0]
        self.assertEqual(project_data['title'], self.project.title)
        self.assertEqual(project_data['description'], self.project.description)
        self.assertEqual(project_data['technologies'], self.project.technologies)

    def test_create_project(self):
        """
        Ensure we can create a new project.
        """
        data = {
            "title": "New API Project",
            "description": "A brand new project created via API.",
            "technologies": "Django REST Framework"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2) # Verify the new project was saved

        # Verify the data of the newly created project
        new_project = Project.objects.get(id=response.data['id'])
        self.assertEqual(new_project.title, data['title'])
