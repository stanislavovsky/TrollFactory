#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv

from trollfactory import factory
from trollfactory.exceptions import InvalidDatasetException, \
                                    InvalidStaticPropertyException, \
                                    UnresolvedDependencyException

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv('ALLOW_ORIGINS', '').split(','),
    allow_credentials=False,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
)


@app.get('/datasets')
async def available_datasets():
    return factory.list_available_datasets()


@app.post('/generate')
async def generate_person(dataset: str = 'pl_PL',
                          localized: bool = False,
                          request: Request = None):
    try:
        req_body = await request.json()
    except Exception:
        req_body = {}

    static_properties = req_body.get('static_properties', {})
    exclude_properties = req_body.get('exclude_properties', [])

    try:
        person = factory.Person(
            dataset=dataset,
            static_properties=static_properties,
            exclude_properties=exclude_properties,
        )
    except InvalidDatasetException:
        raise HTTPException(status_code=404, detail='Dataset unavailable')

    try:
        person.generate()
    except InvalidStaticPropertyException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except UnresolvedDependencyException as exception:
        raise HTTPException(status_code=500, detail=str(exception))
    except Exception as exception:
        raise HTTPException(status_code=500,
                            detail=f'Server-side error: {str(exception)}')

    return person.localized() if localized else person.person