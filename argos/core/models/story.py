from argos.datastore import db
from argos.core.models import Entity
from argos.core.models.cluster import Cluster
from argos.core.brain.cluster import cluster
from argos.core.brain.summarize import multisummarize

from argos.util.logger import logger

stories_events = db.Table('stories_events',
        db.Column('story_id', db.Integer, db.ForeignKey('story.id'), primary_key=True),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

stories_entities = db.Table('stories_entities',
        db.Column('entity_slug', db.String, db.ForeignKey('entity.slug')),
        db.Column('story_id', db.Integer, db.ForeignKey('story.id'))
)

class Story(Cluster):
    __tablename__   = 'story'
    __members__     = {'class_name': 'Event', 'secondary': stories_events, 'backref_name': 'stories'}
    __entities__    = {'secondary': stories_entities, 'backref_name': 'stories'}

    @property
    def events(self):
        """
        Convenience :)
        """
        return self.members

    @events.setter
    def events(self, value):
        self.members = value

    def summarize(self):
        """
        Generate a summary for this cluster.
        """
        if len(self.members) == 1:
            self.summary = self.members[0].summary
        else:
            self.summary = ' '.join(multisummarize([m.summary for m in self.members]))
        return self.summary

    @staticmethod
    def cluster(events, threshold=0.7, debug=False):
        """
        Clusters a set of events
        into existing stories (or creates new ones).

        Args:
            | events (list)         -- the Events to cluster
            | threshold (float)     -- the similarity threshold for qualifying a cluster
            | debug (bool)          -- will log clustering info if True

        Returns:
            | clusters (list)       -- the list of updated clusters
        """
        log = logger('STORY_CLUSTERING')
        if debug:
            log.setLevel('DEBUG')
        else:
            log.setLevel('ERROR')

        updated_clusters = []

        for event in events:
            # Find stories which have some matching entities with this event.
            candidate_clusters = Story.query.filter(Entity.name.in_([entity.name for entity in event.entities])).all()

            # Cluster this event.
            selected_cluster = cluster(event, candidate_clusters, threshold=threshold, logger=log)

            # If no selected cluster was found, then create a new one.
            if not selected_cluster:
                log.debug('No qualifying clusters found, creating a new cluster.')
                selected_cluster = Story([event])
                db.session.add(selected_cluster)

            updated_clusters.append(selected_cluster)

        db.session.commit()
        return updated_clusters
