from __future__ import annotations

from dataclasses import dataclass


@dataclass(eq=True, order=True, frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: object) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)
