BROKER_URL = 'amqp://guest@localhost//'

CELERY_RESULT_BACKEND = 'mongodb'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'celery',

    # What collection to store task metadata.
    'taskmeta_collection': 'taskmeta'
}

# What modules to import on start.
CELERY_IMPORTS = ('tasks','digester.wikidigester',)

# Propagate chord errors when they come up.
CELERY_CHORD_PROPAGATES = True
