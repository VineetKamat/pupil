import os
import sys


if __name__ == "__main__":
    print("Invoke tests by running:")
    print("$ pytest -v {}".format(__file__))
    exit(1)


from .surface import Surface
from .surface import Surface_Marker_Aggregate

from .surface_serializer import _Surface_Serializer_Base
from .surface_serializer import _Surface_Serializer_V00
from .surface_serializer import _Surface_Serializer_V01

from .test_fixtures import (
    SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_1_DIST,
    SURFACE_V00_SERIALIZED,

    SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_1_DIST,
    SURFACE_V00_DESERIALIZED,

    SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_1_DIST,
    SURFACE_V01_SQUARE_SERIALIZED,

    SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_1_DIST,
    SURFACE_V01_SQUARE_DESERIALIZED,

    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_1_DIST,
    SURFACE_V01_APRILTAG_SERIALIZED,

    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_0_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_1_UNDIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_0_DIST,
    SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_1_DIST,
    SURFACE_V01_APRILTAG_DESERIALIZED,
)


def _test_surface_serializer(serializer, surface_pair, marker_aggregate_pairs):

    assert isinstance(serializer, _Surface_Serializer_Base)

    deserialized_surface, serialized_surface = surface_pair
    assert isinstance(deserialized_surface, Surface)
    assert isinstance(serialized_surface, dict)

    for deserialized_aggregate, serialized_aggregate in marker_aggregate_pairs:

        assert isinstance(deserialized_aggregate, Surface_Marker_Aggregate)
        assert isinstance(serialized_aggregate, dict)

        serialization_result = serializer.dict_from_surface_marker_aggregate(deserialized_aggregate)
        assert serialization_result == serialized_aggregate

        deserialization_result = serializer.surface_marker_aggregate_from_dict(serialized_aggregate)
        assert deserialization_result == deserialized_aggregate

    assert serializer.dict_from_surface(
        surface=deserialized_surface,
    ) == serialized_surface

    deserialized_surface_result = serializer.surface_from_dict(
        surface_class=type(deserialized_surface),
        surface_definition=serialized_surface,
    )
    assert Surface.property_equality(deserialized_surface_result, deserialized_surface)


def test_surface_serializer_V00():
    _test_surface_serializer(
        serializer=_Surface_Serializer_V00(),
        surface_pair=(SURFACE_V00_DESERIALIZED, SURFACE_V00_SERIALIZED),
        marker_aggregate_pairs=[
            (SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_0_DIST, SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_0_DIST),
            (SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_1_DIST, SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_1_DIST),
            (SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_0_UNDIST, SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_0_UNDIST),
            (SURFACE_MARKER_AGGREGATE_V00_DESERIALIZED_1_UNDIST, SURFACE_MARKER_AGGREGATE_V00_SERIALIZED_1_UNDIST),
        ]
    )


def test_surface_serializer_V01_square():
    _test_surface_serializer(
        serializer=_Surface_Serializer_V01(),
        surface_pair=(SURFACE_V01_SQUARE_DESERIALIZED, SURFACE_V01_SQUARE_SERIALIZED),
        marker_aggregate_pairs=[
            (SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_0_DIST, SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_0_DIST),
            (SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_1_DIST, SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_1_DIST),
            (SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_0_UNDIST, SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_0_UNDIST),
            (SURFACE_MARKER_AGGREGATE_V01_SQUARE_DESERIALIZED_1_UNDIST, SURFACE_MARKER_AGGREGATE_V01_SQUARE_SERIALIZED_1_UNDIST),
        ]
    )


def test_surface_serializer_V01_apriltag():
    _test_surface_serializer(
        serializer=_Surface_Serializer_V01(),
        surface_pair=(SURFACE_V01_APRILTAG_DESERIALIZED, SURFACE_V01_APRILTAG_SERIALIZED),
        marker_aggregate_pairs=[
            (SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_0_DIST, SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_0_DIST),
            (SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_1_DIST, SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_1_DIST),
            (SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_0_UNDIST, SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_0_UNDIST),
            (SURFACE_MARKER_AGGREGATE_V01_APRILTAG_DESERIALIZED_1_UNDIST, SURFACE_MARKER_AGGREGATE_V01_APRILTAG_SERIALIZED_1_UNDIST),
        ]
    )
