# TrollFactory

**An amazingly accurate fake personality generator.**

## About
TrollFactory is a fairly advanced fake personality generator written in Python. It aims to generate as much data about a person as possible. At the moment it only supports Polish personalities, we're finishing US dataset soon.

## Installation
TrollFactory is available as a PyPI package: `pip3 install TrollFactory`

## Usage

### TrollFactory CLI
The TrollFactory PyPI package also contains TrollFactory CLI. It's currently the most reliable way of using TrollFactory.<br>
To use it, run the `trollfactory` binary from your terminal emulator.

If ran without any parameters, it will generate a personality with default options (Polish dataset, female gender).

At the moment, you can specify a custom dataset and gender (support for other static properties is coming soon):<br>
`trollfactory --gender male --dataset english_us`<br>

You can also generate many personalities at once:<br>
`trollfactory --amount 10`

You can run `trollfactory --help` to read the full help.

### Python library
After installing the TrollFactory Python package, you can use it in your scripts.
```python
import trollfactory.functions as tf
tf.generate_personality('polish', 'male')
```
The `generate_personality()` function returns a dict with generated data.
