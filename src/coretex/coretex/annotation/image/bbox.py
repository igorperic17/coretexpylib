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

from typing import Final, List, Dict
from typing_extensions import Self

from ....codable import Codable, KeyDescriptor


class BBox(Codable):

    """
        Bounding Box as a python class with utility methods

        Properties
        ----------
        minX : float
            top left x coordinate
        minY : float
            top left y coordinate
        width : float
            width of the bounding box
        height : float
            height of the bounding box
    """

    def __init__(self, minX: float = 0, minY: float = 0, width: float = 0, height: float = 0) -> None:
        self.minX: Final = minX
        self.minY: Final = minY

        self.width: Final = width
        self.height: Final = height

    @property
    def maxX(self) -> float:
        """
            Returns
            -------
            float -> bottom right x coordinate
        """

        return self.minX + self.width

    @property
    def maxY(self) -> float:
        """
            Returns
            -------
            float -> bottom right y coordinate
        """

        return self.minY + self.height

    @property
    def polygon(self) -> List[float]:
        """
            Returns
            -------
            List[float] -> Bounding box represented as a polygon (x, y) values
        """

        return [
            self.minX, self.minY,  # top left
            self.maxX, self.minY,  # top right
            self.maxX, self.maxY,  # bottom right
            self.minX, self.maxY,  # bottom left
            self.minX, self.minY   # top left
        ]

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()

        descriptors["minX"] = KeyDescriptor("top_left_x")
        descriptors["minY"] = KeyDescriptor("top_left_y")

        return descriptors

    @classmethod
    def create(cls, minX: float, minY: float, maxX: float, maxY: float) -> Self:
        """
            Utility constructor which has maxX and maxY as parameters instead
            of width and height

            Parameters
            ----------
            minX : float
                top left x coordinate
            minY : float
                top left y coordinate
            maxX : float
                bottom right x coordinate
            maxY : float
                bottom right y coordinate

            Returns
            -------
            Self -> bounding box
        """

        return cls(minX, minY, maxX - minX, maxY - minY)

    @classmethod
    def fromPoly(cls, polygon: List[float]) -> Self:
        """
            Creates bounding box from a polygon, by finding
            the minimum x and y coordinates and calculating
            width and height of the polygon

            Parameters
            ----------
            polygon : List[float]
                list of x, y points - length must be even

            Returns
            -------
            Self -> bounding box

            Example
            -------
            >>> from coretex import Bbox
            \b
            >>> polygon = [0, 0, 0, 3, 4, 3, 4, 0]
            >>> bbox = Bbox.fromPoly(polygon)
            >>> print(f"minX: {bbox.minX}, minY: {bbox.minY}, width: {bbox.width}, height: {bbox.height}")
            "minX: 0, minY: 0, width: 4, height: 3"
        """

        x: List[float] = []
        y: List[float] = []

        for index, value in enumerate(polygon):
            if index % 2 == 0:
                x.append(value)
            else:
                y.append(value)

        return cls.create(min(x), min(y), max(x), max(y))
