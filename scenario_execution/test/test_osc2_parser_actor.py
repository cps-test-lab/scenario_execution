# Copyright (C) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""
Test actor parsing
"""
import unittest
import py_trees
from scenario_execution.model.osc2_parser import OpenScenario2Parser
from scenario_execution.utils.logging import Logger
from antlr4.InputStream import InputStream


class TestOSC2Parser(unittest.TestCase):
    # pylint: disable=missing-function-docstring, protected-access, no-member, unused-variable

    def setUp(self) -> None:
        self.parser = OpenScenario2Parser(Logger('test', False))
        self.tree = py_trees.composites.Sequence()

    def parse(self, scenario_content):
        parsed_tree = self.parser.parse_input_stream(InputStream(scenario_content))
        return self.parser.create_internal_model(parsed_tree, self.tree, "test.osc", False)

    def test_actor(self):
        scenario_content = """
actor base:
    param1: string = "value1"
"""
        model = self.parse(scenario_content)
        self.assertEqual(model._ModelElement__children[0].actor, "base")
        self.assertEqual(model._ModelElement__children[0]._ModelElement__children[0].get_resolved_value(), "value1")

    def test_actor_inheritance(self):
        scenario_content = """
actor base:
    param1: string = "value1"
actor derived inherits base:
    param2: string = "value2"
"""
        model = self.parse(scenario_content)
        self.assertEqual(model._ModelElement__children[0]._ModelElement__children[0].get_resolved_value(), "value1")
        self.assertEqual(model._ModelElement__children[1]._ModelElement__children[1].get_resolved_value(), "value2")

    def test_actor_inheritance_override(self):  # TODO: expected?
        scenario_content = """
actor base:
    param1: string = "value1"
actor derived inherits base:
    param1: string = "OVERRIDE"
    param2: string = "value2"
"""
        model = self.parse(scenario_content)
        params = model._ModelElement__children[1].get_resolved_value()
        self.assertEqual({'param1': 'OVERRIDE', 'param2': 'value2'}, params)
