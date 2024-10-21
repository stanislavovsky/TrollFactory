#!/usr/bin/env python3
from trollfactory import factory
from fastapi import FastAPI

app = FastAPI()


@app.get('/generate')
async def root():
    person = factory.Person('pl_PL')
    person.generate()
    return person.person