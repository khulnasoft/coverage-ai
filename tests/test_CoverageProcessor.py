import pytest
import xml.etree.ElementTree as ET
from coverage_ai.CoverageProcessor import CoverageProcessor


@pytest.fixture
def mock_xml_tree(monkeypatch):
    """
    Creates a mock function to simulate the ET.parse method, returning a mocked XML tree structure.
    """

    def mock_parse(file_path):
        # Mock XML structure for the test
        xml_str = """<coverage>
                        <packages>
                            <package>
                                <classes>
                                    <class filename="app.py">
                                        <lines>
                                            <line number="1" hits="1"/>
                                            <line number="2" hits="0"/>
                                        </lines>
                                    </class>
                                </classes>
                            </package>
                        </packages>
                     </coverage>"""
        root = ET.ElementTree(ET.fromstring(xml_str))
        return root

    monkeypatch.setattr(ET, "parse", mock_parse)


class TestCoverageProcessor:
    @pytest.fixture
    def processor(self):
        # Initializes CoverageProcessor with cobertura coverage type for each test
        return CoverageProcessor("fake_path", "app.py", "cobertura")

    def test_parse_coverage_report_cobertura(self, mock_xml_tree, processor):
        """
        Tests the parse_coverage_report method for correct line number and coverage calculation with Cobertura reports.
        """
        covered_lines, missed_lines, coverage_pct = processor.parse_coverage_report()

        assert covered_lines == [1], "Should list line 1 as covered"
        assert missed_lines == [2], "Should list line 2 as missed"
        assert coverage_pct == 0.5, "Coverage should be 50 percent"

    def test_verify_report_update_file_not_updated(self, mocker):
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('os.path.getmtime', return_value=1234567.0)

        processor = CoverageProcessor("fake_path", "app.py", "cobertura")
        with pytest.raises(AssertionError, match='Fatal: The coverage report file was not updated after the test command.'):
            processor.verify_report_update(1234567890)


    def test_verify_report_update_file_not_exist(self, mocker):
        mocker.patch('os.path.exists', return_value=False)

        processor = CoverageProcessor("fake_path", "app.py", "cobertura")
        with pytest.raises(AssertionError, match='Fatal: Coverage report "fake_path" was not generated.'):
            processor.verify_report_update(1234567890)


    def test_process_coverage_report(self, mocker):
        mock_verify = mocker.patch('coverage_ai.CoverageProcessor.CoverageProcessor.verify_report_update')
        mock_parse = mocker.patch('coverage_ai.CoverageProcessor.CoverageProcessor.parse_coverage_report', return_value=([], [], 0.0))

        processor = CoverageProcessor("fake_path", "app.py", "cobertura")
        result = processor.process_coverage_report(1234567890)

        mock_verify.assert_called_once_with(1234567890)
        mock_parse.assert_called_once()
        assert result == ([], [], 0.0), "Expected result to be ([], [], 0.0)"


    def test_parse_missed_covered_lines_jacoco_key_error(self, mocker):
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='PACKAGE,CLASS,LINE_MISSED,LINE_COVERED\ncom.example,MyClass,5,10'))
        mocker.patch('csv.DictReader', return_value=[
            {'PACKAGE': 'com.example', 'CLASS': 'MyClass', 'LINE_MISSED': '5'}])  # Missing 'LINE_COVERED'

        processor = CoverageProcessor("path/to/coverage_report.csv", "path/to/MyClass.java", "jacoco")

        with pytest.raises(KeyError):
            processor.parse_missed_covered_lines_jacoco("com.example", "MyClass")
