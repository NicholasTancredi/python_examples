"""
    File with simple examples of most common use cases for:
    - unittest
    - pytypes
    - pydantic
    - typing
    - enum
"""
from unittest import TextTestRunner, TestLoader, TestCase
from argparse import ArgumentParser
from pytypes import typechecked
from pydantic import validator, BaseModel, PydanticValueError
from typing import NamedTuple, Tuple, Union
from enum import Enum

# NOTE: Used in get_line_distance
from math import hypot


@typechecked
class Point(NamedTuple):
    y: int
    x: int


@typechecked
class Line(NamedTuple):
    start: Point
    end: Point


@typechecked
def get_line_distance(line: Line) -> float:
    """
        # NOTE: a NamedTuple can still be accessed by index like a regular tuple, for example:
        return hypot(
            line[1][1] - line[0][1],
            line[1][0] - line[0][0]
        )
    """
    return hypot(
        line.end.x - line.start.x,
        line.end.y - line.start.y
    )


@typechecked
def WARNING_DONT_WRITE_LIKE_THIS_get_line_distance(line: Tuple[Tuple[int, int], Tuple[int, int]]) -> float:
    """
        NOTE: using the raw type 'get_line_distance' would be written like this.
        Looking at the type for line:
        "Tuple[Tuple[int, int], Tuple[int, int]]"
        you can see how opaque the input becomes.
    """
    return hypot(
        line[1][1] - line[0][1],
        line[1][0] - line[0][0]
    )


# NOTE: In edge cases you may want to accept all types of input
@typechecked
def get_line_distance_polytype(line: Union[Line, Tuple[Point, Point], Tuple[Tuple[int, int], Tuple[int, int]]]) -> float:
    return hypot(
        line[1][1] - line[0][1],
        line[1][0] - line[0][0]
    )


# Reference material for enums - https://docs.python.org/3/library/enum.html#creating-an-enum
# It is important to note that enums are functional constants. We should refra
    # Note Nomenclature
    # The class TextAlign is an enumeration (or enum)
    # The attributes TextAlign.left, TextAlign.center, etc., are enumeration members (or enum members) and are functionally constants.
    # The enum members have names and values (the name of TextAlign.left is left, the value of TextAlign.hidden is 0, etc.)

@typechecked
class TextAlign(Enum):
    left: str = 'left'
    right: str = 'right'
    center: str = 'center'
    #used to highlight the difference between name and value in enums
    hidden: int = 0


@typechecked
def pad_text(text: str, text_align: TextAlign = TextAlign.left, width: int = 20, fillchar: str = '-') -> str:
    """
        This also has an example of a "python" switch statement equivalent using a dict
    """

    psuedo_switch_statement = {
        TextAlign.left: text.ljust(width, fillchar),
        TextAlign.right: text.rjust(width, fillchar),
        TextAlign.center: text.center(width, fillchar),
    }
    return psuedo_switch_statement[text_align]


class AuthorizationError(PydanticValueError):
    code = 'AuthorizationError'
    msg_template = 'AuthorizationError: the Bearer token provided was invalid. value={value}'


# NOTE: Doesn't need @typechecked for type checking
class Header(BaseModel):
    Authorization: str

    @validator('Authorization')
    def validate_auth(cls, value: str) -> str:
        if value != 'Bearer {}'.format('SECRET_KEY'):
            raise AuthorizationError(value=value)
        return value


if __name__ == '__main__':
    parse = ArgumentParser()

    parse.add_argument(
        '--unittest',
        action='store_true'
    )

    args = parse.parse_args()

    if args.unittest:
        class Test(TestCase):
            def test_get_line_distance(self):
                distance_a = get_line_distance(
                    line=Line(
                        start=Point(
                            y=1,
                            x=2
                        ),
                        end=Point(
                            y=3,
                            x=4
                        )
                    )
                )

                # Less verbose example of calling get_line_distance
                distance_b = get_line_distance(Line(Point(1, 2), Point(3, 4)))
                print('distance_b: ', distance_b)

                # NOTE: WARNING! This is not an example how I'd recommend writing this!
                distance_c = get_line_distance_polytype(((1, 2), (3, 4)))
                distance_d = WARNING_DONT_WRITE_LIKE_THIS_get_line_distance(((1, 2), (3, 4)))

                self.assertEqual(
                    distance_a,
                    distance_b
                )
                self.assertEqual(
                    distance_a,
                    distance_c
                )
                self.assertEqual(
                    distance_a,
                    distance_d
                )

            def test_pad_text(self):
                padded_text = pad_text('yolo', text_align = TextAlign.center)
                print('padded_text: ', padded_text)
                self.assertEqual(
                    padded_text,
                    '--------yolo--------'
                )

            def test_header(self):
                json_input = {
                    'Authorization': 'Bearer {}'.format('SECRET_KEY')
                }
                header = Header(**json_input)
                print('header.json(): ', header.json())
                self.assertDictEqual(
                    json_input,
                    header.dict()
                )
                # NOTE: Input does not have to be json, (i.e. is equivalent)
                header = Header(
                    Authorization='Bearer {}'.format('SECRET_KEY')
                )
                self.assertDictEqual(
                    json_input,
                    header.dict()
                )

        TextTestRunner().run(TestLoader().loadTestsFromTestCase(Test))
