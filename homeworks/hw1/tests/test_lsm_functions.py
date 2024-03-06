import pytest

from pytest import approx

from lsm_project.lsm.functions import (
    get_lsm_description,
    get_lsm_lines,
    get_report,
)
from lsm_project.lsm.models import LSMDescription, LSMLines

from tests.data import (
    wrong_abscissa, wrong_ordinates,
    wrong_args_exceptions, description_wrong_ids,
    strategies, strategies_exception, strategies_ids,
    abscissa, ordinates, descriptions, computition_ids,
    descriptions_incorrect, descriptions_incorrect_ids,
    descriptions_correct, lines_expected, descriptions_correct_ids,
    report_expected
)


@pytest.mark.parametrize(
    'abscissa,ordinates,exception',
    zip(
        wrong_abscissa, wrong_ordinates, wrong_args_exceptions
    ),
    ids=description_wrong_ids
)
def test_get_lsm_description_validation(abscissa, ordinates, exception):
    with pytest.raises(exception):
        get_lsm_description(abscissa, ordinates)


@pytest.mark.parametrize(
    'strategy,exception',
    zip(strategies, strategies_exception),
    ids=strategies_ids
)
def test_get_lsm_description_missmatch(strategy, exception):
    abscissa, ordinates = list(range(3)), list(range(4))

    with pytest.raises(exception):
        get_lsm_description(abscissa, ordinates, strategy)


@pytest.mark.parametrize(
    'ordinates,description_expected',
    zip(ordinates, descriptions),
    ids=computition_ids
)
def test_get_lsm_description_computitions(ordinates, description_expected):
    description = get_lsm_description(abscissa, ordinates)
    precision = 3

    assert isinstance(description, LSMDescription)

    incline = round(description.incline, precision)
    shift = round(description.shift, precision)
    incline_error = round(description.incline_error, precision)
    shift_error = round(description.shift_error, precision)

    assert incline == approx(description_expected.incline)
    assert shift == approx(description_expected.shift)
    assert incline_error == approx(description_expected.incline_error)
    assert shift_error == approx(description_expected.shift_error)


@pytest.mark.parametrize(
    'description', descriptions_incorrect,
    ids=descriptions_incorrect_ids
)
def test_get_lsm_lines_description_incorrect(description):
    with pytest.raises(TypeError):
        get_lsm_lines([], [], description)


@pytest.mark.parametrize(
    'description,lines_expected',
    zip(descriptions_correct, lines_expected),
    ids=descriptions_correct_ids
)
def test_get_lsm_lines_computition(description, lines_expected):
    lines = get_lsm_lines(abscissa, ordinates[-1], description)

    assert isinstance(lines, LSMLines)

    line_predicted = lines.line_predicted
    line_above = lines.line_above
    line_under = lines.line_under

    assert line_predicted == approx(lines_expected.line_predicted)
    assert line_above == approx(lines_expected.line_above)
    assert line_under == approx(lines_expected.line_under)


def test_get_report():
    lsm_description = LSMDescription(
        incline=5.070,
        shift=2.016,
        incline_error=0.081,
        shift_error=0.099
    )

    report = get_report(lsm_description)

    assert report == report_expected


def test_get_report_save_report(mock_builtin_open):
    open_mock = mock_builtin_open

    lsm_description = LSMDescription(
        incline=5.070,
        shift=2.016,
        incline_error=0.081,
        shift_error=0.099
    )

    report = get_report(lsm_description, 'report.txt')
    assert report == report_expected

    open_mock.assert_called_once()
    handle = open_mock()
    handle.write.assert_called_once()
