from tests.helpers import save
from argos.core.models import Entity, Article, Event, Story, Source
from argos.web.models import User
from argos.datastore import db

from copy import copy

def user(num=1):
    args = {
            'name': 'Hubble Bubble {0}',
            'email': 'hubbubs{0}@mail.com',
            'image': 'https://hubb.ub/pic{0}.png',
            'active': True,
            'password': '123456'
    }
    u_s = []
    for i in range(num):
        # Copy the args and fill in
        # the numbers.
        a = copy(args)
        for k, v in a.items():
            if isinstance(a[k], str):
                a[k] = v.format(i)
        u_s.append(User(**a))

    save(u_s)

    if len(u_s) is 1:
        return u_s[0]
    return u_s


def entity(num=1):
    args = [
        {'name': 'Argos'},
        {'name': 'Ceres'},
        {'name': 'Iliad'}
    ]
    e_s = [Entity(**args[i]) for i in range(num)]

    save(e_s)

    if len(e_s) is 1:
        return e_s[0]
    return e_s

def source(num=1):
    args = [
        {'url': 'foo'},
        {'url': 'bar'},
        {'url': 'sup'}
    ]
    s_s = [Source(**args[i]) for i in range(num)]

    save(s_s)

    if len(s_s) is 1:
        return s_s[0]
    return s_s

def article(num=1, **kwargs):
    args = [
        {'title':'Dinosaurs', 'text':'Dinosaurs are cool, Clinton'},
        {'title':'Robots', 'text':'Robots are nice, Clinton'},
        {'title':'Mudcrabs', 'text':'Mudcrabs are everywhere, Clinton'}
    ]

    if not kwargs:
        a_s = [Article(**args[i]) for i in range(num)]
    else:
        a_s = [Article(**kwargs) for i in range(num)]

    save(a_s)

    if len(a_s) is 1:
        return a_s[0]
    return a_s

def event(num=1, num_members=2):
    """
    Creates an event cluster.
    """
    return cluster(
            cls=Event,
            member_factory=article,
            num=num,
            num_members=num_members
    )

def story(num=1, num_members=2):
    """
    Creates a story cluster.
    """
    return cluster(
            cls=Story,
            member_factory=event,
            num=num,
            num_members=num_members
    )

def cluster(cls, member_factory, num=1, num_members=2):
    """
    Convenience method for creating a Cluster-like object.

    Args:
        | cls (class)           -- a Cluster-like class
        | member_factory (func) -- function for creating members
        | num (int)             -- number of clusters to create
        | num_members (int)     -- number of members in each cluster
    """
    c_s = []
    for i in range(num):
        members = member_factory(num=num_members)
        c = cls(members)
        c_s.append(c)
    save(c_s)
    if len(c_s) is 1:
        return c_s[0]
    return c_s
