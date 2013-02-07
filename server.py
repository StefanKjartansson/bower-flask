#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick and dirty bower component server.
"""
from __future__ import unicode_literals, print_function, absolute_import

import json
import os

from flask import Flask, request, abort, make_response, Response
from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
db_name = 'packages.db'
Base = declarative_base()
engine = create_engine('sqlite:///%s' % db_name)
session = scoped_session(sessionmaker(bind=engine))


def json_response(content, status=200):
    return Response(json.dumps(content),
        status=status, mimetype='application/json')


class Package(Base):
    __tablename__ = 'packages'
    created_at = Column(DateTime, default=func.now())
    name = Column(String(64), primary_key=True, unique=True, index=True)
    url = Column(String(64))
    hits = Column(Integer, default=0)

    def as_json(self):
        return {'name': self.name, 'url': self.url}


@app.route('/packages', methods=['GET', 'POST'])
def packages():
    if request.method == 'GET':
        return json_response([i.as_json() for i in session.query(Package)
            .order_by(Package.name).all()])

    url = request.form['url']
    if not url.startswith('git:'):
        abort(400)
    p = Package(name=request.form['name'], url=url)
    try:
        session.add(p)
        session.commit()
    except IntegrityError:
        session.rollback()
        abort(406)
    return make_response('', 201)


@app.route('/packages/<name>', methods=['GET'])
def get_packages(name):
    p = session.query(Package).get(name)
    if not p:
        abort(404)
    p.hits += 1
    session.add(p)
    session.commit()
    return json_response(p.as_json())


@app.route('/packages/search/<name>', methods=['GET'])
def search_packages(name):
    return json_response([i.as_json() for i in session.query(Package)
        .filter(Package.name.ilike(name)).order_by(Package.hits).all()])


if __name__ == "__main__":
    if not os.path.exists(db_name):
        Base.metadata.create_all(bind=engine)
    app.run()
