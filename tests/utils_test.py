# test_utils.py

from unittest import TestCase
from jinja2 import Environment, FileSystemLoader


class TryTesting(TestCase):
    def test_functor_is_not_mapping_type(self):

        functor = lambda ctx: ctx['x'] + ctx['y'],

        j2_template="""
        {%- import 'utils.j2' as utils -%}
        {{ utils.is_functor(functor) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(functor=functor)
        self.assertEqual(result, 'False')

    def test_functor_is_mapping_type_but_has_not_function_key_defined(self):

        functor = { 'foo': lambda ctx: ctx['x'] + ctx['y'] }

        j2_template="""
        {%- import 'utils.j2' as utils -%}
        {{ utils.is_functor(functor) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(functor=functor)
        self.assertEqual(result, 'False')

    def test_functor_is_mapping_type_and_has_function_key_defined_but_not_ctx_key(self):

        functor = { 'function': lambda ctx: ctx['x'] + ctx['y'] }

        j2_template="""
        {%- import 'utils.j2' as utils -%}
        {{ utils.is_functor(functor) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(functor=functor)
        self.assertEqual(result, 'False')

    def test_functor_is_mapping_type_and_has_both_ctx_and_function_key_defined_but_function_is_not_callable(self):

        functor = { 'ctx': 'This is your context to be pass in', 'function': 'NOT_CALLABLE' }

        j2_template="""
        {%- import 'utils.j2' as utils -%}
        {{ utils.is_functor(functor) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(functor=functor)
        self.assertEqual(result, 'False')

    def test_a_right_functor_is_passed(self):

        functor = {
            'ctx': {
                'x': 1,
                'y': 2,
            },
            'function': lambda ctx: ctx['x'] + ctx['y'],
        }

        j2_template="""
        {%- import 'utils.j2' as utils -%}
        {{ utils.is_functor(functor) }} - {{ functor.function(functor.ctx) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(functor=functor)
        self.assertEqual(result, f'True - {functor["ctx"]["x"] + functor["ctx"]["y"]}')
