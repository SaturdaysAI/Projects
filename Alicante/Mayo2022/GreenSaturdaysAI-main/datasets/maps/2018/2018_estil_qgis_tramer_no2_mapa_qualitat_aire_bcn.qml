<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" styleCategories="AllStyleCategories" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" minScale="100000000" simplifyDrawingHints="1" readOnly="0" version="3.14.15-Pi" maxScale="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal durationField="" startExpression="" enabled="0" endExpression="" fixedDuration="0" startField="" endField="" durationUnit="min" mode="0" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="categorizedSymbol" enableorderby="0" forceraster="0" attr="Rang" symbollevels="0">
    <categories>
      <category value="&lt;= 20 µg/m³" render="true" symbol="0" label="&lt;= 20 µg/m³"/>
      <category value="20 - 30 µg/m³" render="true" symbol="1" label="20 - 30 µg/m³"/>
      <category value="30 - 40 µg/m³" render="true" symbol="2" label="30 - 40 µg/m³"/>
      <category value="40 - 50 µg/m³" render="true" symbol="3" label="40 - 50 µg/m³"/>
      <category value="50 - 60 µg/m³" render="true" symbol="4" label="50 - 60 µg/m³"/>
      <category value="60 - 70 µg/m³" render="true" symbol="5" label="60 - 70 µg/m³"/>
      <category value="> 70 µg/m³" render="true" symbol="6" label="> 70 µg/m³"/>
    </categories>
    <symbols>
      <symbol alpha="1" type="line" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="2" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="3" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,136,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="4" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="5" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="128,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="6" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="128,0,200,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol alpha="1" type="line" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="CASE&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=750 THEN 1.5&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=2000 THEN 1&#xd;&#xa;&#x9;WHEN  @map_scale &lt;=7500 THEN 0.7&#xd;&#xa;&#x9;ELSE 0.5&#xd;&#xa;END" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp type="gradient" name="[source]">
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
    <property value="TRAM" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory diagramOrientation="Up" minScaleDenominator="0" minimumSize="0" barWidth="5" height="15" spacing="0" scaleDependency="Area" opacity="1" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" backgroundColor="#ffffff" showAxis="0" spacingUnitScale="3x:0,0,0,0,0,0" penColor="#000000" spacingUnit="MM" sizeScale="3x:0,0,0,0,0,0" width="15" sizeType="MM" penWidth="0" rotationOffset="270" direction="1" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" backgroundAlpha="255" lineSizeType="MM" penAlpha="255" enabled="0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
      <axisSymbol>
        <symbol alpha="1" type="line" name="" clip_to_extent="1" force_rhr="0">
          <layer pass="0" enabled="1" class="SimpleLine" locked="0">
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
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
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" obstacle="0" dist="0" priority="0" placement="2" zIndex="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
  <fieldConfiguration>
    <field name="TRAM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rang">
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
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="TRAM" applyOnUpdate="0" expression=""/>
    <default field="Rang" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="TRAM" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="Rang" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="TRAM"/>
    <constraint desc="" exp="" field="Rang"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;NO2 2018 def&quot;">
    <columns>
      <column type="field" width="-1" hidden="0" name="TRAM"/>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" width="-1" hidden="0" name="Rang"/>
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
    <field editable="1" name="FFCC_DIA"/>
    <field editable="1" name="FFCC_NIT"/>
    <field editable="1" name="FFCC_VES"/>
    <field editable="1" name="GI_TR_DIA"/>
    <field editable="1" name="GI_TR_NIT"/>
    <field editable="1" name="GI_TR_VES"/>
    <field editable="1" name="INDUST_DIA"/>
    <field editable="1" name="INDUST_NIT"/>
    <field editable="1" name="INDUST_VES"/>
    <field editable="1" name="NO2 2018 def"/>
    <field editable="1" name="NO2_18"/>
    <field editable="0" name="NO2_18 fin"/>
    <field editable="1" name="OCI_NIT"/>
    <field editable="1" name="PATIS_DIA"/>
    <field editable="1" name="PATIS_VES"/>
    <field editable="1" name="Rang"/>
    <field editable="1" name="TOTAL_DIA"/>
    <field editable="1" name="TOTAL_NIT"/>
    <field editable="1" name="TOTAL_VES"/>
    <field editable="1" name="TRAM"/>
    <field editable="1" name="TRANSIT_D"/>
    <field editable="1" name="TRANSIT_N"/>
    <field editable="1" name="TRANSIT_V"/>
    <field editable="1" name="VIANANTS_D"/>
    <field editable="1" name="VIANANTS_V"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="lateral"/>
    <field editable="1" name="modificat"/>
    <field editable="1" name="ronda"/>
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
