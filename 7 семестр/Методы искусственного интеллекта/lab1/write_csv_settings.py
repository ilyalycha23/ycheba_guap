from pathlib import Path

abs_path = "D:/KNIME/lab1_data/Salary_Data.csv"
NS = (
    'xmlns="http://www.knime.org/2008/09/XMLConfig" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    'xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig '
    'http://www.knime.org/XMLConfig_2008_09.xsd"'
)
q = "&quot;"
xml = f"""<?xml version="1.0" encoding="UTF-8"?>
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
                    <entry key="convenience_fs_category" type="xstring" value="LOCAL"/>
                    <entry key="relative_to" type="xstring" value="knime.workflow.data"/>
                    <entry key="mountpoint" type="xstring" value="LOCAL"/>
                    <entry key="spaceId" type="xstring" value=""/>
                    <entry key="spaceName" type="xstring" value=""/>
                    <entry key="custom_url_timeout" type="xint" value="10000"/>
                    <entry key="connected_fs" type="xboolean" value="true"/>
                </config>
                <config key="path">
                    <entry key="location_present" type="xboolean" value="true"/>
                    <entry key="file_system_type" type="xstring" value="LOCAL"/>
                    <entry key="path" type="xstring" value="{abs_path}"/>
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
            <entry key="quote_char" type="xstring" value="{q}"/>
            <entry key="quote_escape_char" type="xstring" value="{q}"/>
            <entry key="use_line_break_row_delimiter" type="xboolean" value="true"/>
            <entry key="row_delimiter" type="xstring" value="%%00010"/>
            <entry key="autodetect_buffer_size" type="xint" value="1048576"/>
        </config>
        <entry key="fail_on_differing_specs" type="xboolean" value="false"/>
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
</config>
"""
p = Path(
    r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1"
    r"\knime_workspace\Lab1_Linear_Regression\CSV Reader (#1)\settings.xml"
)
p.write_text(xml, encoding="utf-8")
print("written", p.stat().st_size, abs_path in p.read_text(encoding="utf-8"))
