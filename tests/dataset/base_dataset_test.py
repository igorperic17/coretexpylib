#     Copyright (C) 2023  BioMech LLC

#     This file is part of Coretex.ai  

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Type

import unittest
import time

from coretex import Dataset, Sample


class BaseDatasetTest:

    class Base(unittest.TestCase):

        dataset: Dataset[Sample]
        sampleType: Type

        def test_sampleType(self) -> None:
            for sample in self.dataset.samples:
                self.assertIsInstance(sample, self.sampleType)

        def test_count(self) -> None:
            self.assertEqual(self.dataset.count, len(self.dataset.samples))

        def test_rename(self) -> None:
            newName = f"PythonUnitTest {time.time()}"
            self.dataset.rename(newName)

            self.assertEqual(self.dataset.name, newName)
