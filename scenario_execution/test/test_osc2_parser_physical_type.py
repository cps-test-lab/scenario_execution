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
Test physical type parsing
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

    def test_success(self):
        scenario_content = """

type length is SI(m: 1)
unit m          of length is SI(m: 1, factor: 1)
type time is SI(s: 1)
unit s          of time is SI(s: 1, factor: 1)

action odometry_distance_traveled:
    distance: length = 3m
"""
        model = self.parse(scenario_content)
        action = model._ModelElement__children[4].get_resolved_value()
        self.assertEqual({'distance': 3.0}, action)

    def test_wrong_type(self):
        scenario_content = """

type length is SI(m: 1)
unit m          of length is SI(m: 1, factor: 1)
type time is SI(s: 1)
unit s          of time is SI(s: 1, factor: 1)

action odometry_distance_traveled:
    distance: length = 3s
"""
        parsed_tree = self.parser.parse_input_stream(InputStream(scenario_content))
        self.assertRaises(ValueError, self.parser.create_internal_model, parsed_tree, self.tree, "test.osc")
