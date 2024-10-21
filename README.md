<p align="center">
  <img width="550" src="logo.png" alt="TrollFactory"/>
</p>

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/25a087b7553145a99df141287a47ce9c)](https://app.codacy.com/gh/stanislavovsky/TrollFactory/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![GitHub License](https://img.shields.io/github/license/stanislavovsky/TrollFactory)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/stanislavovsky/TrollFactory)
![GitHub repo size](https://img.shields.io/github/repo-size/stanislavovsky/TrollFactory)

*Rewrite coming soon, stay tuned!*

TrollFactory is an extensible fake personalities generator aiming to produce large amounts of coherent and plausible data that can be easily tailored for various use cases. It utilizes interchangeable datasets containing collections of open-source data on the demographics and topography of different regions.

## Install

A PyPI package is being released with the first stable version of TrollFactory 3.x. If you want to try it out right now, you can simply clone this repository:

```bash
git clone git@github.com:stanislawowski/TrollFactory.git -b rewrite
```

And use the library in your Python 3 shell/projects:

```python
from trollfactory import factory
person = factory.Person('pl_PL', static_properties={'sex': {'sex': 'female'}})
person.generate()
```