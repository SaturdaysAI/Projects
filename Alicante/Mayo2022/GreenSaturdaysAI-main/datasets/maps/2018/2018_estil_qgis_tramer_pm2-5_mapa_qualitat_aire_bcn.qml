<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="100000000" simplifyDrawingHints="1" labelsEnabled="0" version="3.16.0-Hannover" simplifyMaxScale="1" styleCategories="AllStyleCategories" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyLocal="1" maxScale="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal fixedDuration="0" accumulate="0" enabled="0" startExpression="" startField="" endExpression="" durationUnit="min" endField="" mode="0" durationField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" enableorderby="0" attr="Rang" type="categorizedSymbol" symbollevels="0">
    <categories>
      <category render="true" value="&lt;= 10 µg/m³" label="&lt;= 10 µg/m³" symbol="0"/>
      <category render="true" value="10 - 15 µg/m³" label="10 - 15 µg/m³" symbol="1"/>
      <category render="true" value="15 - 20 µg/m³" label="15 - 20 µg/m³" symbol="2"/>
      <category render="true" value="20 - 25 µg/m³" label="20 - 25 µg/m³" symbol="3"/>
      <category render="true" value="> 25 µg/m³" label="> 25 µg/m³" symbol="4"/>
    </categories>
    <symbols>
      <symbol name="0" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="43,131,186,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="128,191,172,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="199,233,173,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,205,105,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="81,185,109,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp name="[source]" type="gradient">
      <prop v="43,131,186,255" k="color1"/>
      <prop v="227,26,28,255" k="color2"/>
      <prop v="0" k="discrete"/>
      <prop v="gradient" k="rampType"/>
      <prop v="0.25;171,221,164,255:0.5;255,255,191,255:0.75;253,174,97,255" k="stops"/>
    </colorramp>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>TRAM</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory penColor="#000000" maxScaleDenominator="1e+08" scaleDependency="Area" height="15" rotationOffset="270" lineSizeScale="3x:0,0,0,0,0,0" showAxis="0" sizeScale="3x:0,0,0,0,0,0" enabled="0" spacingUnitScale="3x:0,0,0,0,0,0" minScaleDenominator="0" barWidth="5" backgroundColor="#ffffff" penAlpha="255" penWidth="0" scaleBasedVisibility="0" lineSizeType="MM" opacity="1" labelPlacementMethod="XHeight" backgroundAlpha="255" spacing="0" spacingUnit="MM" diagramOrientation="Up" width="15" minimumSize="0" sizeType="MM" direction="1">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
      <axisSymbol>
        <symbol name="" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
          <layer locked="0" pass="0" enabled="1" class="SimpleLine">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" placement="2" dist="0" priority="0" zIndex="0" linePlacementFlags="18" obstacle="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="TRAM" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rang" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="TRAM" index="0"/>
    <alias name="" field="Rang" index="1"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="TRAM"/>
    <default applyOnUpdate="0" expression="" field="Rang"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="TRAM"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="Rang"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="TRAM"/>
    <constraint desc="" exp="" field="Rang"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="&quot;TRAM&quot;">
    <columns>
      <column name="TRAM" width="-1" hidden="0" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column name="Rang" width="-1" hidden="0" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">O:/Qualitat Ambiental/_00_Soroll/Mapa Estratègic 2017/31. QVISTA</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>O:/Qualitat Ambiental/_00_Soroll/Mapa Estratègic 2017/31. QVISTA</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="FFCC_DIA" editable="1"/>
    <field name="FFCC_NIT" editable="1"/>
    <field name="FFCC_VES" editable="1"/>
    <field name="GI_TR_DIA" editable="1"/>
    <field name="GI_TR_NIT" editable="1"/>
    <field name="GI_TR_VES" editable="1"/>
    <field name="INDUST_DIA" editable="1"/>
    <field name="INDUST_NIT" editable="1"/>
    <field name="INDUST_VES" editable="1"/>
    <field name="NO2 2018 def" editable="1"/>
    <field name="NO2_18" editable="1"/>
    <field name="NO2_18 fin" editable="0"/>
    <field name="OCI_NIT" editable="1"/>
    <field name="PATIS_DIA" editable="1"/>
    <field name="PATIS_VES" editable="1"/>
    <field name="PM10 18 c" editable="1"/>
    <field name="PM10 2018" editable="1"/>
    <field name="PM2,5 2018" editable="1"/>
    <field name="Rang" editable="1"/>
    <field name="TOTAL_DIA" editable="1"/>
    <field name="TOTAL_NIT" editable="1"/>
    <field name="TOTAL_VES" editable="1"/>
    <field name="TRAM" editable="1"/>
    <field name="TRANSIT_D" editable="1"/>
    <field name="TRANSIT_N" editable="1"/>
    <field name="TRANSIT_V" editable="1"/>
    <field name="VIANANTS_D" editable="1"/>
    <field name="VIANANTS_V" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="lateral" editable="1"/>
    <field name="modificat" editable="1"/>
    <field name="ronda" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="FFCC_DIA" labelOnTop="0"/>
    <field name="FFCC_NIT" labelOnTop="0"/>
    <field name="FFCC_VES" labelOnTop="0"/>
    <field name="GI_TR_DIA" labelOnTop="0"/>
    <field name="GI_TR_NIT" labelOnTop="0"/>
    <field name="GI_TR_VES" labelOnTop="0"/>
    <field name="INDUST_DIA" labelOnTop="0"/>
    <field name="INDUST_NIT" labelOnTop="0"/>
    <field name="INDUST_VES" labelOnTop="0"/>
    <field name="NO2 2018 def" labelOnTop="0"/>
    <field name="NO2_18" labelOnTop="0"/>
    <field name="NO2_18 fin" labelOnTop="0"/>
    <field name="OCI_NIT" labelOnTop="0"/>
    <field name="PATIS_DIA" labelOnTop="0"/>
    <field name="PATIS_VES" labelOnTop="0"/>
    <field name="PM10 18 c" labelOnTop="0"/>
    <field name="PM10 2018" labelOnTop="0"/>
    <field name="PM2,5 2018" labelOnTop="0"/>
    <field name="Rang" labelOnTop="0"/>
    <field name="TOTAL_DIA" labelOnTop="0"/>
    <field name="TOTAL_NIT" labelOnTop="0"/>
    <field name="TOTAL_VES" labelOnTop="0"/>
    <field name="TRAM" labelOnTop="0"/>
    <field name="TRANSIT_D" labelOnTop="0"/>
    <field name="TRANSIT_N" labelOnTop="0"/>
    <field name="TRANSIT_V" labelOnTop="0"/>
    <field name="VIANANTS_D" labelOnTop="0"/>
    <field name="VIANANTS_V" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="lateral" labelOnTop="0"/>
    <field name="modificat" labelOnTop="0"/>
    <field name="ronda" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"TRAM"</previewExpression>
  <mapTip>ID_NIVELL</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
