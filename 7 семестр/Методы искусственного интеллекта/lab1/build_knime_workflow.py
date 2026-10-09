"""Build Lab1 Linear Regression KNIME workflow on disk."""
from __future__ import annotations

import shutil
from pathlib import Path
from textwrap import dedent

WS = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\knime_workspace")
SRC = WS / "_downloads" / "knime2py" / "repo" / "knime2py-main" / "tests" / "data"
INZ = SRC / "INZ_visa_decisions_model"
EX_CSV = WS / "Example Workflows" / "Basic Examples" / "Building a Simple Classifier" / "CSV Reader (#14)" / "settings.xml"
DATA_SRC = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\data\Salary_Data.csv")
OUT = WS / "Lab1_Linear_Regression"

NS = 'xmlns="http://www.knime.org/2008/09/XMLConfig" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig http://www.knime.org/XMLConfig_2008_09.xsd"'


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def node_shell(name: str, factory: str, model_xml: str, extra: str = "") -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config {NS} key="settings.xml">
    <entry key="node_file" type="xstring" value="settings.xml"/>
    <config key="flow_stack"/>
    <config key="internal_node_subsettings">
        <entry key="memory_policy" type="xstring" value="CacheSmallInMemory"/>
    </config>
    <config key="model">
{model_xml}
    </config>
    <config key="nodeAnnotation">
        <entry key="text" type="xstring" value="{name}"/>
        <entry key="contentType" type="xstring" value="text/plain"/>
        <entry key="bgcolor" type="xint" value="16777215"/>
        <entry key="x-coordinate" type="xint" value="0"/>
        <entry key="y-coordinate" type="xint" value="0"/>
        <entry key="width" type="xint" value="100"/>
        <entry key="height" type="xint" value="15"/>
        <entry key="alignment" type="xstring" value="CENTER"/>
        <entry key="borderSize" type="xint" value="0"/>
        <entry key="borderColor" type="xint" value="16777215"/>
        <entry key="defFontSize" type="xint" value="9"/>
        <entry key="annotation-version" type="xint" value="20151123"/>
        <config key="styles"/>
    </config>
    <entry key="customDescription" type="xstring" isnull="true" value=""/>
    <entry key="state" type="xstring" value="IDLE"/>
    <entry key="factory" type="xstring" value="{factory}"/>
    <entry key="node-name" type="xstring" value="{name}"/>
    <entry key="node-bundle-name" type="xstring" value="KNIME Base Nodes"/>
    <entry key="node-bundle-symbolic-name" type="xstring" value="org.knime.base"/>
    <entry key="node-bundle-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-bundle-version" type="xstring" value="5.12.0.v202606261225"/>
    <entry key="node-feature-name" type="xstring" value="KNIME Base nodes"/>
    <entry key="node-feature-symbolic-name" type="xstring" value="org.knime.features.base.feature.group"/>
    <entry key="node-feature-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-feature-version" type="xstring" value="5.12.0.v202606261225"/>
    <config key="factory_settings"/>
    {extra}
    <entry key="name" type="xstring" value="{name}"/>
    <entry key="hasContent" type="xboolean" value="false"/>
    <entry key="isInactive" type="xboolean" value="false"/>
    <config key="ports"/>
    <config key="filestores">
        <entry key="file_store_location" type="xstring" isnull="true" value=""/>
        <entry key="file_store_id" type="xstring" isnull="true" value=""/>
    </config>
</config>'''


def csv_reader_xml() -> str:
    # Based on example CSV Reader, simplified for Salary_Data.csv under workflow/data
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config {NS} key="settings.xml">
    <entry key="node_file" type="xstring" value="settings.xml"/>
    <config key="flow_stack"/>
    <config key="internal_node_subsettings">
        <entry key="memory_policy" type="xstring" value="CacheSmallInMemory"/>
    </config>
    <config key="model">
        <config key="settings">
            <config key="file_selection_Internals">
                <entry key="SettingsModelID" type="xstring" value="SMID_ReaderFileChooser"/>
                <entry key="EnabledStatus" type="xboolean" value="true"/>
            </config>
            <config key="file_selection">
                <config key="file_system_chooser__Internals">
                    <entry key="has_fs_port" type="xboolean" value="false"/>
                    <entry key="overwritten_by_variable" type="xboolean" value="false"/>
                    <entry key="convenience_fs_category" type="xstring" value="RELATIVE"/>
                    <entry key="relative_to" type="xstring" value="knime.workflow"/>
                    <entry key="mountpoint" type="xstring" value="LOCAL"/>
                    <entry key="spaceId" type="xstring" value=""/>
                    <entry key="spaceName" type="xstring" value=""/>
                    <entry key="custom_url_timeout" type="xint" value="1000"/>
                    <entry key="connected_fs" type="xboolean" value="true"/>
                </config>
                <config key="path">
                    <entry key="location_present" type="xboolean" value="true"/>
                    <entry key="file_system_type" type="xstring" value="RELATIVE"/>
                    <entry key="file_system_specifier" type="xstring" value="knime.workflow"/>
                    <entry key="path" type="xstring" value="data/Salary_Data.csv"/>
                </config>
                <config key="filter_mode_Internals">
                    <entry key="SettingsModelID" type="xstring" value="SMID_FilterMode"/>
                    <entry key="EnabledStatus" type="xboolean" value="true"/>
                </config>
                <config key="filter_mode">
                    <entry key="filter_mode" type="xstring" value="FILE"/>
                    <entry key="include_subfolders" type="xboolean" value="false"/>
                    <config key="filter_options">
                        <entry key="filter_files_extension" type="xboolean" value="false"/>
                        <entry key="files_extension_expression" type="xstring" value=""/>
                        <entry key="files_extension_case_sensitive" type="xboolean" value="false"/>
                        <entry key="filter_files_name" type="xboolean" value="false"/>
                        <entry key="files_name_expression" type="xstring" value="*"/>
                        <entry key="files_name_case_sensitive" type="xboolean" value="false"/>
                        <entry key="files_name_filter_type" type="xstring" value="WILDCARD"/>
                        <entry key="include_hidden_files" type="xboolean" value="false"/>
                        <entry key="include_special_files" type="xboolean" value="true"/>
                        <entry key="filter_folders_name" type="xboolean" value="false"/>
                        <entry key="folders_name_expression" type="xstring" value="*"/>
                        <entry key="folders_name_case_sensitive" type="xboolean" value="false"/>
                        <entry key="folders_name_filter_type" type="xstring" value="WILDCARD"/>
                        <entry key="include_hidden_folders" type="xboolean" value="false"/>
                        <entry key="follow_links" type="xboolean" value="true"/>
                    </config>
                </config>
            </config>
            <entry key="has_column_header" type="xboolean" value="true"/>
            <entry key="has_row_id" type="xboolean" value="false"/>
            <entry key="support_short_data_rows" type="xboolean" value="false"/>
            <entry key="skip_empty_data_rows" type="xboolean" value="false"/>
            <entry key="prepend_file_idx_to_row_id" type="xboolean" value="false"/>
            <entry key="comment_char" type="xstring" value="#"/>
            <entry key="column_delimiter" type="xstring" value=","/>
            <entry key="quote_char" type="xstring" value="&quot;"/>
            <entry key="quote_escape_char" type="xstring" value="&quot;"/>
            <entry key="use_line_break_row_delimiter" type="xboolean" value="true"/>
            <entry key="row_delimiter" type="xstring" value="%%00013%%00010"/>
            <entry key="autodetect_buffer_size" type="xint" value="1048576"/>
        </config>
        <config key="table_spec_config_Internals">
            <entry key="version" type="xstring" value="V4_4"/>
            <config key="individual_specs">
                <config key="data/Salary_Data.csv">
                    <entry key="num_columns" type="xint" value="3"/>
                    <config key="0">
                        <entry key="name" type="xstring" value="Employee"/>
                        <entry key="has_type" type="xboolean" value="true"/>
                        <config key="type">
                            <entry key="class" type="xstring" value="java.lang.Integer"/>
                        </config>
                    </config>
                    <config key="1">
                        <entry key="name" type="xstring" value="YearsExperience"/>
                        <entry key="has_type" type="xboolean" value="true"/>
                        <config key="type">
                            <entry key="class" type="xstring" value="java.lang.Double"/>
                        </config>
                    </config>
                    <config key="2">
                        <entry key="name" type="xstring" value="Salary"/>
                        <entry key="has_type" type="xboolean" value="true"/>
                        <config key="type">
                            <entry key="class" type="xstring" value="java.lang.Double"/>
                        </config>
                    </config>
                </config>
            </config>
            <config key="table_specification">
                <entry key="num_columns" type="xint" value="3"/>
                <config key="0">
                    <entry key="name" type="xstring" value="Employee"/>
                    <entry key="type" type="xstring" value="Number (integer)"/>
                </config>
                <config key="1">
                    <entry key="name" type="xstring" value="YearsExperience"/>
                    <entry key="type" type="xstring" value="Number (double)"/>
                </config>
                <config key="2">
                    <entry key="name" type="xstring" value="Salary"/>
                    <entry key="type" type="xstring" value="Number (double)"/>
                </config>
            </config>
        </config>
        <entry key="fail_on_differing_specs" type="xboolean" value="true"/>
        <entry key="append_path_column" type="xboolean" value="false"/>
        <entry key="path_column_name" type="xstring" value="File Path"/>
    </config>
    <config key="nodeAnnotation">
        <entry key="text" type="xstring" value="Salary_Data.csv"/>
        <entry key="contentType" type="xstring" value="text/plain"/>
        <entry key="bgcolor" type="xint" value="16777215"/>
        <entry key="x-coordinate" type="xint" value="0"/>
        <entry key="y-coordinate" type="xint" value="0"/>
        <entry key="width" type="xint" value="100"/>
        <entry key="height" type="xint" value="15"/>
        <entry key="alignment" type="xstring" value="CENTER"/>
        <entry key="borderSize" type="xint" value="0"/>
        <entry key="borderColor" type="xint" value="16777215"/>
        <entry key="defFontSize" type="xint" value="9"/>
        <entry key="annotation-version" type="xint" value="20151123"/>
        <config key="styles"/>
    </config>
    <entry key="customDescription" type="xstring" isnull="true" value=""/>
    <entry key="state" type="xstring" value="IDLE"/>
    <entry key="factory" type="xstring" value="org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory"/>
    <entry key="node-name" type="xstring" value="CSV Reader"/>
    <entry key="node-bundle-name" type="xstring" value="KNIME Base Nodes"/>
    <entry key="node-bundle-symbolic-name" type="xstring" value="org.knime.base"/>
    <entry key="node-bundle-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-bundle-version" type="xstring" value="5.12.0.v202606261225"/>
    <entry key="node-feature-name" type="xstring" value="KNIME Base nodes"/>
    <entry key="node-feature-symbolic-name" type="xstring" value="org.knime.features.base.feature.group"/>
    <entry key="node-feature-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-feature-version" type="xstring" value="5.12.0.v202606261225"/>
    <config key="factory_settings"/>
    <entry key="name" type="xstring" value="CSV Reader"/>
    <entry key="hasContent" type="xboolean" value="false"/>
    <entry key="isInactive" type="xboolean" value="false"/>
    <config key="ports"/>
    <config key="filestores">
        <entry key="file_store_location" type="xstring" isnull="true" value=""/>
        <entry key="file_store_id" type="xstring" isnull="true" value=""/>
    </config>
</config>'''


def workflow_knime() -> str:
    # IDs: 1 CSV, 2 Color, 3 Partition, 4 Learner, 5 Predictor, 6 Scorer, 7 Scatter
    nodes = [
        (1, "CSV Reader (#1)", 80, 200),
        (2, "Color Manager (#2)", 260, 200),
        (3, "Partitioning (#3)", 440, 200),
        (4, "Linear Regression Learner (#4)", 640, 120),
        (5, "Regression Predictor (#5)", 860, 200),
        (6, "Numeric Scorer (#6)", 1080, 120),
        (7, "Scatter Plot (#7)", 1080, 280),
    ]
    node_xml = []
    for nid, folder, x, y in nodes:
        node_xml.append(f'''        <config key="node_{nid}">
            <entry key="id" type="xint" value="{nid}"/>
            <entry key="node_settings_file" type="xstring" value="{folder}/settings.xml"/>
            <entry key="node_is_meta" type="xboolean" value="false"/>
            <entry key="node_type" type="xstring" value="NativeNode"/>
            <entry key="ui_classname" type="xstring" value="org.knime.core.node.workflow.NodeUIInformation"/>
            <config key="ui_settings">
                <config key="extrainfo.node.bounds">
                    <entry key="array-size" type="xint" value="4"/>
                    <entry key="0" type="xint" value="{x}"/>
                    <entry key="1" type="xint" value="{y}"/>
                    <entry key="2" type="xint" value="120"/>
                    <entry key="3" type="xint" value="80"/>
                </config>
            </config>
        </config>''')

    # Connections (ports are 1-based in workflow.knime for data ports)
    # CSV(1)->Color(2) data
    # Color(2)->Part(3) data (port 1)
    # Part(3) train port1 -> Learner(4) port1
    # Part(3) test port2 -> Predictor(5) port2
    # Learner(4) model port1 -> Predictor(5) port1
    # Predictor(5) -> Scorer(6), Scatter(7)
    conns = [
        (1, 2, 1, 1),
        (2, 3, 1, 1),
        (3, 4, 1, 1),
        (3, 5, 2, 2),
        (4, 5, 1, 1),
        (5, 6, 1, 1),
        (5, 7, 1, 1),
    ]
    conn_xml = []
    for i, (s, d, sp, dp) in enumerate(conns):
        conn_xml.append(f'''        <config key="connection_{i}">
            <entry key="sourceID" type="xint" value="{s}"/>
            <entry key="destID" type="xint" value="{d}"/>
            <entry key="sourcePort" type="xint" value="{sp}"/>
            <entry key="destPort" type="xint" value="{dp}"/>
        </config>''')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config {NS} key="workflow.knime">
    <entry key="created_by" type="xstring" value="5.12.0.v202606180846"/>
    <entry key="created_by_nightly" type="xboolean" value="false"/>
    <entry key="version" type="xstring" value="5.1.0"/>
    <entry key="name" type="xstring" isnull="true" value=""/>
    <config key="authorInformation">
        <entry key="authored-by" type="xstring" value="ilyal"/>
        <entry key="authored-when" type="xstring" value="2026-10-09 22:20:00 +0300"/>
        <entry key="lastEdited-by" type="xstring" value="ilyal"/>
        <entry key="lastEdited-when" type="xstring" value="2026-10-09 22:20:00 +0300"/>
    </config>
    <entry key="customDescription" type="xstring" value="Lab1 Linear Regression Salary ~ YearsExperience"/>
    <entry key="state" type="xstring" value="IDLE"/>
    <config key="workflow_credentials"/>
    <config key="annotations">
        <config key="annotation_0">
            <entry key="text" type="xstring" value="&lt;p&gt;&lt;strong&gt;LR1. Linear Regression&lt;/strong&gt;&lt;/p&gt;&lt;p&gt;Прогнозирование зарплаты на основе стажа работы (YearsExperience). Обучающая выборка — 20%, линейная выборка.&lt;/p&gt;"/>
            <entry key="contentType" type="xstring" value="text/html"/>
            <entry key="bgcolor" type="xint" value="16777215"/>
            <entry key="x-coordinate" type="xint" value="60"/>
            <entry key="y-coordinate" type="xint" value="20"/>
            <entry key="width" type="xint" value="700"/>
            <entry key="height" type="xint" value="70"/>
            <entry key="alignment" type="xstring" value="LEFT"/>
            <entry key="borderSize" type="xint" value="8"/>
            <entry key="borderColor" type="xint" value="16766976"/>
            <entry key="defFontSize" type="xint" value="-1"/>
            <entry key="annotation-version" type="xint" value="20230412"/>
            <config key="styles"/>
        </config>
    </config>
    <config key="nodes">
{chr(10).join(node_xml)}
    </config>
    <config key="connections">
{chr(10).join(conn_xml)}
    </config>
    <config key="workflow_editor_settings">
        <entry key="workflow.editor.snapToGrid" type="xboolean" value="true"/>
        <entry key="workflow.editor.ShowGrid" type="xboolean" value="true"/>
        <entry key="workflow.editor.gridX" type="xint" value="20"/>
        <entry key="workflow.editor.gridY" type="xint" value="20"/>
        <entry key="workflow.editor.zoomLevel" type="xdouble" value="1.0"/>
        <entry key="workflow.editor.curvedConnections" type="xboolean" value="true"/>
        <entry key="workflow.editor.connectionWidth" type="xint" value="2"/>
    </config>
</config>'''


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    data_dir = OUT / "data"
    data_dir.mkdir()
    shutil.copy2(DATA_SRC, data_dir / "Salary_Data.csv")

    write(OUT / "CSV Reader (#1)" / "settings.xml", csv_reader_xml())

    write(
        OUT / "Color Manager (#2)" / "settings.xml",
        node_shell(
            "Color Manager",
            "org.knime.base.node.viz.property.color.ColorManager2NodeFactory",
            '''        <entry key="selected_column" type="xstring" value="Salary"/>
        <entry key="is_nominal" type="xboolean" value="false"/>
        <entry key="min_color" type="xint" value="-13369600"/>
        <entry key="max_color" type="xint" value="-16776961"/>''',
        ),
    )

    write(
        OUT / "Partitioning (#3)" / "settings.xml",
        node_shell(
            "Partitioning",
            "org.knime.base.node.preproc.partition.PartitionNodeFactory",
            '''        <entry key="method" type="xstring" value="Relative"/>
        <entry key="samplingMethod" type="xstring" value="Linear"/>
        <entry key="fraction" type="xdouble" value="0.2"/>
        <entry key="count" type="xint" value="100"/>
        <entry key="random_seed" type="xstring" isnull="true" value=""/>
        <entry key="class_column" type="xstring" value="Salary"/>''',
        ),
    )

    write(
        OUT / "Linear Regression Learner (#4)" / "settings.xml",
        node_shell(
            "Linear Regression Learner",
            "org.knime.base.node.mine.regression.linear2.learner.LinReg2LearnerNodeFactory2",
            '''        <entry key="target" type="xstring" value="Salary"/>
        <config key="column_filter">
            <entry key="filter-type" type="xstring" value="STANDARD"/>
            <config key="included_names">
                <entry key="array-size" type="xint" value="1"/>
                <entry key="0" type="xstring" value="YearsExperience"/>
            </config>
            <config key="excluded_names">
                <entry key="array-size" type="xint" value="2"/>
                <entry key="0" type="xstring" value="Employee"/>
                <entry key="1" type="xstring" value="Salary"/>
            </config>
            <entry key="enforce_option" type="xstring" value="EnforceExclusion"/>
            <config key="name_pattern">
                <entry key="pattern" type="xstring" value=""/>
                <entry key="type" type="xstring" value="Wildcard"/>
                <entry key="caseSensitive" type="xboolean" value="true"/>
                <entry key="excludeMatching" type="xboolean" value="false"/>
            </config>
            <config key="datatype">
                <config key="typelist">
                    <entry key="org.knime.core.data.StringValue" type="xboolean" value="false"/>
                    <entry key="org.knime.core.data.DoubleValue" type="xboolean" value="false"/>
                    <entry key="org.knime.core.data.BooleanValue" type="xboolean" value="false"/>
                    <entry key="org.knime.core.data.IntValue" type="xboolean" value="false"/>
                    <entry key="org.knime.core.data.LongValue" type="xboolean" value="false"/>
                    <entry key="org.knime.core.data.date.DateAndTimeValue" type="xboolean" value="false"/>
                </config>
            </config>
        </config>
        <entry key="include_constant" type="xboolean" value="true"/>
        <entry key="offset_value" type="xdouble" value="0.0"/>
        <entry key="missing_value_handling" type="xstring" value="fail"/>
        <entry key="scatter_plot_first_row" type="xint" value="1"/>
        <entry key="scatter_plot_row_count" type="xint" value="20000"/>''',
        ),
    )

    write(
        OUT / "Regression Predictor (#5)" / "settings.xml",
        node_shell(
            "Regression Predictor",
            "org.knime.base.node.mine.regression.predict3.RegressionPredictorNodeFactory2",
            '''        <entry key="has_custom_predicition_name" type="xboolean" value="false"/>
        <entry key="custom_prediction_name" type="xstring" isnull="true" value=""/>
        <entry key="include_probabilites" type="xboolean" value="false"/>
        <entry key="propability_columns_suffix" type="xstring" value=""/>''',
        ),
    )

    write(
        OUT / "Numeric Scorer (#6)" / "settings.xml",
        node_shell(
            "Numeric Scorer",
            "org.knime.base.node.mine.scorer.numeric2.NumericScorer2NodeFactory",
            '''        <config key="reference_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_string"/>
            <entry key="EnabledStatus" type="xboolean" value="true"/>
        </config>
        <config key="reference">
            <entry key="useRowID" type="xboolean" value="false"/>
            <entry key="columnName" type="xstring" value="Salary"/>
        </config>
        <config key="predicted_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_string"/>
            <entry key="EnabledStatus" type="xboolean" value="true"/>
        </config>
        <config key="predicted">
            <entry key="useRowID" type="xboolean" value="false"/>
            <entry key="columnName" type="xstring" value="Prediction (Salary)"/>
        </config>
        <config key="override default output name_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_boolean"/>
            <entry key="EnabledStatus" type="xboolean" value="true"/>
        </config>
        <entry key="override default output name" type="xboolean" value="false"/>
        <config key="output column_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_string"/>
            <entry key="EnabledStatus" type="xboolean" value="false"/>
        </config>
        <entry key="output column" type="xstring" value="Prediction (Salary)"/>
        <config key="name prefix for flowvars_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_string"/>
            <entry key="EnabledStatus" type="xboolean" value="false"/>
        </config>
        <entry key="name prefix for flowvars" type="xstring" value=""/>
        <config key="generate flow variables_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_boolean"/>
            <entry key="EnabledStatus" type="xboolean" value="true"/>
        </config>
        <entry key="generate flow variables" type="xboolean" value="false"/>
        <config key="number_of_predictors_Internals">
            <entry key="SettingsModelID" type="xstring" value="SMID_integer"/>
            <entry key="EnabledStatus" type="xboolean" value="true"/>
        </config>
        <entry key="number_of_predictors" type="xint" value="1"/>''',
        ),
    )

    write(
        OUT / "Scatter Plot (#7)" / "settings.xml",
        f'''<?xml version="1.0" encoding="UTF-8"?>
<config {NS} key="settings.xml">
    <entry key="node_file" type="xstring" value="settings.xml"/>
    <config key="flow_stack"/>
    <config key="internal_node_subsettings">
        <entry key="memory_policy" type="xstring" value="CacheSmallInMemory"/>
    </config>
    <config key="model">
        <entry key="generateImage" type="xboolean" value="false"/>
        <entry key="imageFormat" type="xstring" value="SVG"/>
        <entry key="width" type="xint" value="800"/>
        <entry key="height" type="xint" value="600"/>
    </config>
    <config key="view">
        <entry key="xAxisColumnV3" type="xstring" value="YearsExperience"/>
        <entry key="yAxisColumnV3" type="xstring" value="Salary"/>
        <entry key="maxRows" type="xint" value="12500"/>
        <entry key="title" type="xstring" value="Salary vs YearsExperience"/>
        <entry key="axisExtentMethod" type="xstring" value="AUTO"/>
        <entry key="dataPointSize" type="xint" value="10"/>
        <entry key="showLegend" type="xboolean" value="true"/>
        <entry key="allowImageDownload" type="xboolean" value="true"/>
        <entry key="enableDataZoom" type="xboolean" value="true"/>
        <entry key="showTooltip" type="xboolean" value="true"/>
        <entry key="enableAnimation" type="xboolean" value="true"/>
        <entry key="xAxisScale" type="xstring" value="VALUE"/>
        <entry key="yAxisScale" type="xstring" value="VALUE"/>
    </config>
    <entry key="customDescription" type="xstring" isnull="true" value=""/>
    <entry key="state" type="xstring" value="IDLE"/>
    <entry key="factory" type="xstring" value="org.knime.base.views.node.scatterplot.ScatterPlotNodeFactory"/>
    <entry key="node-name" type="xstring" value="Scatter Plot"/>
    <entry key="node-bundle-name" type="xstring" value="KNIME Views"/>
    <entry key="node-bundle-symbolic-name" type="xstring" value="org.knime.base.views"/>
    <entry key="node-bundle-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-bundle-version" type="xstring" value="5.12.0.v202606171319"/>
    <entry key="node-feature-name" type="xstring" value="KNIME Views"/>
    <entry key="node-feature-symbolic-name" type="xstring" value="org.knime.features.base.views.feature.group"/>
    <entry key="node-feature-vendor" type="xstring" value="KNIME AG, Zurich, Switzerland"/>
    <entry key="node-feature-version" type="xstring" value="5.12.0.v202606171319"/>
    <config key="factory_settings"/>
    <entry key="name" type="xstring" value="Scatter Plot"/>
    <entry key="hasContent" type="xboolean" value="false"/>
    <entry key="isInactive" type="xboolean" value="false"/>
    <config key="ports"/>
    <config key="filestores">
        <entry key="file_store_location" type="xstring" isnull="true" value=""/>
        <entry key="file_store_id" type="xstring" isnull="true" value=""/>
    </config>
</config>''',
    )

    write(OUT / "workflow.knime", workflow_knime())
    write(
        OUT / "workflow-metadata.xml",
        f'''<?xml version="1.0" encoding="UTF-8"?>
<workflow-metadata {NS} key="workflow-metadata.xml">
    <entry key="metadata-version" type="xint" value="1"/>
    <entry key="description" type="xstring" value="Lab1 Linear Regression"/>
</workflow-metadata>''',
    )
    print("Built workflow at", OUT)


if __name__ == "__main__":
    main()
