# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, Reaction


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('index'))

    def test_create_post_requires_login(self):
        response = self.client.get(reverse('create'))
        self.assertRedirects(response, '/login/?next=/create/')


class PostCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            category='General',
            author=self.user
        )

    def test_index_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(reverse('create'), {
            'title': 'New Post',
            'content': 'New content',
            'category': 'Events'
        })
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_edit_post(self):
        response = self.client.post(reverse('edit', args=[self.post.id]), {
            'title': 'Updated Title',
            'content': 'Updated content',
            'category': 'Housing'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        self.client.get(reverse('delete', args=[self.post.id]))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_category_filter(self):
        Post.objects.create(title='Events Post', content='x', category='Events', author=self.user)
        response = self.client.get(reverse('index') + '?category=Events')
        self.assertContains(response, 'Events Post')
        self.assertNotContains(response, 'Test Post')


class CommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Post', content='Content', category='General', author=self.user
        )

    def test_add_comment(self):
        self.client.post(reverse('add_comment', args=[self.post.id]), {
            'content': 'Great post!'
        })
        self.assertTrue(Comment.objects.filter(content='Great post!').exists())

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Hello')
        self.client.get(reverse('delete_comment', args=[comment.id]))
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())


class ReactionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Post', content='Content', category='General', author=self.user
        )

    def test_add_reaction(self):
        response = self.client.post(reverse('react', args=[self.post.id, '👍']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reaction.objects.filter(post=self.post, author=self.user, emoji='👍').exists())

    def test_toggle_reaction_off(self):
        Reaction.objects.create(post=self.post, author=self.user, emoji='👍')
        self.client.post(reverse('react', args=[self.post.id, '👍']))
        self.assertFalse(Reaction.objects.filter(post=self.post, author=self.user, emoji='👍').exists())

    def test_no_duplicate_reactions(self):
        self.client.post(reverse('react', args=[self.post.id, '❤️']))
        self.client.post(reverse('react', args=[self.post.id, '❤️']))
        count = Reaction.objects.filter(post=self.post, author=self.user, emoji='❤️').count()
        self.assertEqual(count, 0)