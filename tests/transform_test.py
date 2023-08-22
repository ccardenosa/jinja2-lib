# transform_test.py

from unittest import TestCase
from jinja2 import Environment, FileSystemLoader


class TryTesting(TestCase):

    def test_transform_with_function(self):

        power = 2
        f = lambda data: data ** power

        in_list = [1,2,3]
        out_list = [item ** power for item in in_list]

        j2_template="""
        {%- import 'transform.j2' as utils -%}
        {{ utils.transform(in_list, f) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(in_list=in_list, f=f)
        self.assertEqual(result, f'{out_list}')

    def test_transform_with_functor(self):

        functor = {
            'ctx': {
                'power': 2,
            },
            'function': lambda ctx, data: data ** ctx['power'],
        }

        in_list = [1,2,3]
        out_list = [item ** functor['ctx']['power'] for item in in_list]

        j2_template="""
        {%- import 'transform.j2' as utils -%}
        {{ utils.transform(in_list, functor) }}"""

        env = Environment(loader=FileSystemLoader('templates/'))
        t = env.from_string(j2_template)
        result = t.render(in_list=in_list, out_list=out_list, functor=functor)
        self.assertEqual(result, f'{out_list}')
