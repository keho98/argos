import tests.factories as fac
from tests.helpers import save

from tests import RequiresApp

from argos.core.models import Entity, Article, Story

class APITest(RequiresApp):
    def test_404(self):
        r = self.client.get('/does_not_exist')
        self.assertTrue(r.data)
        self.assertEqual(r.status_code, 404)

    def test_GET_entity(self):
        entity = fac.entity()
        r = self.client.get('/entities/{0}'.format(entity.slug))
        expected = {
                'name': entity.name,
                'slug': entity.slug
        }
        self.assertEqual(self.json(r), expected)

    def test_GET_event(self):
        event = fac.event()

        expected_members = []
        entities = []
        for member in event.members:
            expected_members.append({
                'title': member.title,
                'id': member.id,
                'url': member.url,
                'created_at': member.created_at.isoformat()
            })
            for entity in member.entities:
                entities.append({
                    'name': entity.name,
                    'url': '/entities/{0}'.format(entity.slug)
                })

        # Filter down to unique entities.
        expected_entities = list({v['url']:v for v in entities}.values())

        expected = {
                'id': event.id,
                'title': event.title,
                'summary': event.summary,
                'updated_at': event.updated_at.isoformat(),
                'created_at': event.created_at.isoformat(),
                'members': expected_members,
                'entities': expected_entities
        }

        r = self.client.get('/events/{0}'.format(event.id))

        self.assertEqual(self.json(r), expected)

    def test_GET_story(self):
        story = fac.story()

        expected_members = []
        entities = []
        for member in story.members:
            expected_members.append({
                'title': member.title,
                'id': member.id,
                'url': '/events/{0}'.format(member.id),
                'created_at': member.created_at.isoformat()
            })
            for entity in member.entities:
                entities.append({
                    'name': entity.name,
                    'url': '/entities/{0}'.format(entity.slug)
                })

        # Filter down to unique entities.
        expected_entities = list({v['url']:v for v in entities}.values())

        expected = {
                'id': story.id,
                'title': story.title,
                'summary': story.summary,
                'updated_at': story.updated_at.isoformat(),
                'created_at': story.created_at.isoformat(),
                'members': expected_members,
                'entities': expected_entities
        }

        r = self.client.get('/stories/{0}'.format(story.id))

        self.assertEqual(self.json(r), expected)

    def test_GET_story_watchers(self):
        story = fac.story()
        users = fac.user(num=3)
        story.watchers = users
        save()

        expected = []
        for user in users:
            expected.append({
                'id': user.id,
                'name': user.name,
                'image': user.image,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            })

        r = self.client.get('/stories/{0}/watchers'.format(story.id))

        self.assertEqual(self.json(r), {'watchers': expected})

    def test_POST_story_watchers(self):
        story = fac.story()
        users = fac.user(num=4)
        user = users[-1]
        story.watchers = users[:3]
        save()

        self.assertEqual(len(story.watchers), 3)

        # Login the user so we have an authenticated user.
        r = self.client.post('/test_login', data={'id': user.id})

        r = self.client.post('/stories/{0}/watchers'.format(story.id))
        self.assertEqual(len(story.watchers), 4)

    def test_DELETE_story_watchers(self):
        story = fac.story()
        users = fac.user(num=3)
        user = users[0]
        story.watchers = users
        save()

        self.assertEqual(len(story.watchers), 3)

        # Login the user so we have an authenticated user.
        r = self.client.post('/test_login', data={'id': user.id})

        r = self.client.delete('/stories/{0}/watchers'.format(story.id))
        self.assertEqual(len(story.watchers), 2)
