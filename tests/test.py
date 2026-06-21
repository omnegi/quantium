import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#dashboard-header")

    header = dash_duo.find_element("#dashboard-header")

    assert header.text != ""
    assert "Pink Morsel Analytics" in header.text


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#sales-chart")

    graph = dash_duo.find_element("#sales-chart")

    assert graph.is_displayed()


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter")

    region_picker = dash_duo.find_element("#region-filter")

    assert region_picker.is_displayed()

