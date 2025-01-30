# Примеры императивного маппинга

from sqlalchemy import and_, or_
from sqlalchemy.orm import foreign, registry, relationship, remote
from sqlalchemy.orm.collections import keyfunc_mapping

mapper = registry()


mapper.map_imperatively(
    entities.Factory,
    tables.factories,
    properties={
        'factory_type': relationship(
            entities.FactoryType, uselist=False, lazy='joined', viewonly=True
        ),
        'organization_unit': relationship(
            entities.OrganizationUnit, uselist=False, lazy='raise'
        ),
    }
)

mapper.map_imperatively(
    entities.EstimateIndicator,
    tables.estimate_indicators,
    properties={
        'facility_props': relationship(
            entities.IndicatorFacilityProps,
            collection_class=keyfunc_mapping(
                lambda prop: (
                    prop.factory_type_id,
                    prop.factory_unit_id,
                    prop.division_unit_id,
                )
            ),
            lazy='subquery'
        ),
        'factory_types': relationship(
            entities.FactoryType,
            secondary=tables.indicator_types,
            uselist=True,
            lazy='joined',
            overlaps="display_settings"
        ),
        'plan_sae': relationship(
            entities.PlanAreaEstimate,
            uselist=True,
            lazy='raise',
            back_populates='estimate_indicator',
            viewonly=True
        ),
        'display_settings': relationship(
            entities.IndicatorTypeSettings,
            collection_class=keyfunc_mapping(
                lambda settings: settings.factory_type_id
            ),
            lazy='joined',
            uselist=True,
            viewonly=True,
            overlaps="factory_types"
        )
    }
)

base_fact_estimate_mapper = mapper.map_imperatively(
    entities.FactEstimate,
    tables.fact_estimates,
    polymorphic_identity='base',
    polymorphic_on=tables.fact_estimates.c.section,
    polymorphic_abstract=True,
    properties={
        'division': relationship(
            entities.DivisionFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                foreign(tables.fact_estimates.c.division_unit_id
                        ) == remote(tables.divisions.c.org_unit_id)
            ),
            viewonly=True,
        ),
        'factory': relationship(
            entities.FactoryFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                foreign(tables.fact_estimates.c.factory_unit_id
                        ) == remote(tables.factories.c.organization_unit_id)
            ),
            viewonly=True,
        ),
        'factory_type': relationship(
            entities.FactoryType,
            uselist=False,
            lazy='raise',
            viewonly=True,
        ),
        'estimate_indicator': relationship(
            entities.EstimateIndicator,
            uselist=False,
            viewonly=True,
            lazy='raise'
        )
    }
)

# yapf: disable
fact_area_estimate_mapper = mapper.map_imperatively(
    entities.FactAreaEstimate,
    inherits=base_fact_estimate_mapper,
    polymorphic_abstract=True,
    properties={
        'plan_estimates': relationship(
            entities.PlanAreaEstimate,
            primaryjoin=(
                and_(
                    foreign(
                        tables.fact_estimates.c.estimate_indicator_id
                    ) == remote(
                        tables.plan_estimates.c.
                        estimate_indicator_id
                    ),
                    tables.fact_estimates.c.estimate_date >=    # noqa: W504
                    tables.plan_estimates.c.active_from
                )
            ),
            lazy='raise',
            uselist=True,
            viewonly=True
        ),
    }
)

# yapf: enable

mapper.map_imperatively(
    entities.FactEstimateIS,
    inherits=fact_area_estimate_mapper,
    polymorphic_identity=constants.Sections.INDUSTRIAL_SAFETY,
)

mapper.map_imperatively(
    entities.FactEstimateWS,
    inherits=fact_area_estimate_mapper,
    polymorphic_identity=constants.Sections.WORK_SAFETY,
)

mapper.map_imperatively(
    entities.FactEstimateSC,
    inherits=fact_area_estimate_mapper,
    polymorphic_identity=constants.Sections.SAFETY_CULTURE,
)


def eq_or_absent(column_foreign, column_remote):
    return or_(
        foreign(column_foreign) == remote(column_remote),
        and_(column_foreign.is_(None), column_remote.is_(None))
    )


mapper.map_imperatively(
    entities.FactDriverEstimate,
    inherits=base_fact_estimate_mapper,
    polymorphic_identity=constants.Sections.DRIVER,
    properties={
        'plan_estimates': relationship(
            entities.PlanDriverEstimate,
            primaryjoin=and_(
                foreign(
                    tables.fact_estimates.c.estimate_indicator_id
                ) == remote(tables.plan_estimates.c.estimate_indicator_id),
                eq_or_absent(
                    tables.fact_estimates.c.division_unit_id,
                    tables.plan_estimates.c.division_unit_id
                ),
                eq_or_absent(
                    tables.fact_estimates.c.factory_unit_id,
                    tables.plan_estimates.c.factory_unit_id
                ),
                eq_or_absent(
                    tables.fact_estimates.c.factory_type_id,
                    tables.plan_estimates.c.factory_type_id
                ),
            ),
            lazy='raise',
            uselist=True,
            viewonly=True
        )
    }
)

base_plan_estimate_mapper = mapper.map_imperatively(
    entities.PlanEstimate,
    tables.plan_estimates,
    polymorphic_on=tables.plan_estimates.c.section,
    properties={
        'estimate_indicator': relationship(
            entities.EstimateIndicator,
            uselist=False,
            lazy='joined',
            viewonly=True
        ),
        'division': relationship(
            entities.DivisionFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                tables.plan_estimates.c.division_unit_id ==    # noqa: W504
                tables.divisions.c.org_unit_id
            ),
            viewonly=True,
        ),
        'factory': relationship(
            entities.FactoryFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                tables.plan_estimates.c.factory_unit_id ==    # noqa: W504
                tables.factories.c.organization_unit_id
            ),
            viewonly=True,
        ),
        'factory_type': relationship(
            entities.FactoryType,
            uselist=False,
            lazy='raise',
            viewonly=True,
        ),
    }
)

mapper.map_imperatively(
    entities.PlanDriverEstimate,
    inherits=base_plan_estimate_mapper,
    polymorphic_identity=constants.Sections.DRIVER,
)

area_plan_mapper = mapper.map_imperatively(
    entities.PlanAreaEstimate,
    inherits=base_plan_estimate_mapper,
    polymorphic_abstract=True,
)

mapper.map_imperatively(
    entities.PlanAreaEstimateIS,
    inherits=area_plan_mapper,
    polymorphic_identity=constants.Sections.INDUSTRIAL_SAFETY
)

mapper.map_imperatively(
    entities.PlanAreaEstimateWS,
    inherits=area_plan_mapper,
    polymorphic_identity=constants.Sections.WORK_SAFETY
)

mapper.map_imperatively(
    entities.PlanAreaEstimateSC,
    inherits=area_plan_mapper,
    polymorphic_identity=constants.Sections.SAFETY_CULTURE
)

mapper.map_imperatively(
    entities.CheckListTemplate,
    tables.check_lists_templates,
    properties={
        'criteria': relationship(
            entities.TemplateCriterion, uselist=True, lazy='subquery'
        ),
        'factory_types': relationship(
            entities.FactoryTypeFacility,
            secondary=tables.facility_templates,
            overlaps="factories,facilities"
        ),
        'factories': relationship(
            entities.FactoryFacility,
            secondary=tables.facility_templates,
            overlaps="factory_types,facilities"
        ),
        'divisions': relationship(
            entities.DivisionFacility,
            secondary=tables.facility_templates,
            overlaps="factory_types,factories"
        ),
        'indicator': relationship(
            entities.EstimateIndicator, uselist=False, lazy='subquery'
        ),
        'acceptors': relationship(
            entities.Employee, secondary=tables.acceptors
        ),
        'check_lists': relationship(
            entities.CheckList,
            uselist=True,
            lazy='select',
            back_populates='template',
            viewonly=True
        ),
        'department_group': relationship(
            entities.DepartmentGroup, uselist=False, lazy='subquery'
        )
    }
)

mapper.map_imperatively(
    entities.TemplateCriterion,
    tables.template_criteria,
    properties={
        'control_params': relationship(
            entities.BaseTemplateCriterionControlParam,
            uselist=True,
            lazy='subquery'
        )
    }
)

base_template_param_mapper = mapper.map_imperatively(
    entities.BaseTemplateCriterionControlParam,
    tables.template_criteria_control_params,
    polymorphic_abstract=True,
    polymorphic_identity='base',
    polymorphic_on=tables.template_criteria_control_params.c.template_type,
    properties={
        'violations': relationship(
            entities.Violation,
            uselist=True,
            secondary=tables.violation_parameters,
            back_populates='control_params'
        )
    }
)

mapper.map_imperatively(
    entities.TemplateCriterionControlParam,
    tables.template_criteria_control_params,
    inherits=base_template_param_mapper,
    polymorphic_identity=constants.TemplateTypes.DEFAULT,
)

mapper.map_imperatively(
    entities.TemplateSPCriterionControlParam,
    tables.template_criteria_control_params,
    inherits=base_template_param_mapper,
    polymorphic_identity=constants.TemplateTypes.SINGLE_PARAM,
)

mapper.map_imperatively(
    entities.CheckList,
    tables.check_lists,
    properties={
        'division': relationship(
            entities.DivisionFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                foreign(tables.check_lists.c.facility_id
                        ) == remote(tables.divisions.c.org_unit_id)
            ),
            viewonly=True,
        ),
        'factory': relationship(
            entities.FactoryFacility,
            uselist=False,
            lazy='raise',
            primaryjoin=(
                foreign(tables.check_lists.c.facility_id
                        ) == remote(tables.factories.c.organization_unit_id)
            ),
            viewonly=True,
        ),
        'template': relationship(
            entities.CheckListTemplate,
            uselist=False,
            lazy='joined',
            back_populates='check_lists'
        ),
        'control_params': relationship(
            entities.BaseCheckListCriterionControlParam,
            uselist=True,
            lazy='subquery'
        ),
        'updates': relationship(
            entities.CheckListUpdate, uselist=True, lazy='subquery'
        ),
        'acceptor': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id == tables.check_lists.c.acceptor_id
            ),
            uselist=False,
            lazy='joined'
        ),
        'verifier': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id == tables.check_lists.c.verifier_id
            ),
            uselist=False,
            lazy='joined'
        ),
        'representative': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id == tables.check_lists.c.representative_id
            ),
            lazy='joined'
        ),
        'department_group': relationship(
            entities.DepartmentGroup, uselist=False, viewonly=True
        )
    }
)

mapper.map_imperatively(
    entities.CheckListTemplateForRating,
    tables.check_lists_templates,
    properties={
        'criteria': relationship(
            entities.TemplateCriterion,
            uselist=True,
            lazy='subquery',
            viewonly=True
        ),
        'indicator': relationship(
            entities.EstimateIndicator,
            uselist=False,
            lazy='subquery',
            viewonly=True
        ),
        'department_group': relationship(
            entities.DepartmentGroup, uselist=False, viewonly=True
        )
    }
)

mapper.map_imperatively(
    entities.CheckListForRating,
    tables.check_lists,
    properties={
        'template': relationship(
            entities.CheckListTemplateForRating,
            uselist=False,
            lazy='joined',
            viewonly=True
        ),
        'control_params': relationship(
            entities.BaseCheckListCriterionControlParam,
            uselist=True,
            lazy='subquery',
            viewonly=True
        )
    }
)

base_checklist_param_mapper = mapper.map_imperatively(
    entities.BaseCheckListCriterionControlParam,
    tables.check_list_criteria_control_params,
    polymorphic_abstract=True,
    polymorphic_identity='base',
    polymorphic_on=tables.check_list_criteria_control_params.c.template_type
)

mapper.map_imperatively(
    entities.CheckListCriterionControlParam,
    tables.check_list_criteria_control_params,
    inherits=base_checklist_param_mapper,
    polymorphic_identity=constants.TemplateTypes.DEFAULT
)

mapper.map_imperatively(
    entities.CheckListSPCriterionControlParam,
    tables.check_list_criteria_control_params,
    inherits=base_checklist_param_mapper,
    polymorphic_identity=constants.TemplateTypes.SINGLE_PARAM
)

mapper.map_imperatively(entities.FacilityTemplate, tables.facility_templates)

mapper.map_imperatively(entities.Employee, tables.employees)
mapper.map_imperatively(
    entities.CheckListAudit,
    tables.check_lists_audit,
    properties={
        'acceptor': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id == tables.check_lists_audit.c.acceptor_id
            ),
            uselist=False,
            lazy='joined'
        ),
        'verifier': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id == tables.check_lists_audit.c.verifier_id
            ),
            uselist=False,
            lazy='joined'
        ),
        'representative': relationship(
            entities.Employee,
            primaryjoin=(
                tables.employees.c.id ==    # noqa: W504
                tables.check_lists_audit.c.representative_id
            )
        )
    }
)
mapper.map_imperatively(
    entities.CheckListControlParamAudit,
    tables.check_list_criteria_control_params_audit
)
mapper.map_imperatively(
    entities.CheckListUpdate,
    tables.check_list_updates,
    properties={
        'check_list_update': relationship(
            entities.CheckListAudit, uselist=False, lazy='joined'
        ),
        'check_list_param_updates': relationship(
            entities.CheckListControlParamAudit, uselist=True, lazy='subquery'
        ),
        'updated_by': relationship(
            entities.Employee, uselist=False, lazy='joined'
        )
    }
)

mapper.map_imperatively(
    entities.OrganizationUnit,
    tables.organization_units,
    properties={
        'parent': relationship(
            entities.OrganizationUnit,
            uselist=False,
            back_populates='children',
            remote_side=tables.organization_units.c.id,
            lazy='raise',
            viewonly=True
        ),
        'children': relationship(
            entities.OrganizationUnit,
            uselist=True,
            back_populates='parent',
            remote_side=tables.organization_units.c.parent_id,
            lazy='subquery',
            join_depth=10,
            viewonly=True
        ),
        'places': relationship(
            entities.OperationPlace,
            uselist=True,
            lazy='subquery',
            viewonly=True
        ),
    }
)
mapper.map_imperatively(
    entities.OperationPlace,
    tables.operation_places,
    properties={
        'division': relationship(
            entities.DivisionFacility,
            primaryjoin=(
                foreign(tables.operation_places.c.organization_unit_id)
                ==    # noqa: W504
                remote(tables.divisions.c.org_unit_id)
            ),
            uselist=False,
            lazy='raise',
            viewonly=True
        )
    }
)
mapper.map_imperatively(entities.EmployeeHSEI, tables.employees_hsei)
mapper.map_imperatively(
    entities.Violation,
    tables.violations,
    properties={
        'control_params': relationship(
            entities.BaseTemplateCriterionControlParam,
            uselist=True,
            secondary=tables.violation_parameters,
            back_populates='violations'
        ),
        'operation_place': relationship(entities.OperationPlace, uselist=False),
        'inspector': relationship(entities.EmployeeHSEI, uselist=False)
    }
)
mapper.map_imperatively(
    entities.ViolationParameter, tables.violation_parameters
)

mapper.map_imperatively(entities.DepartmentGroup, tables.department_groups)
mapper.map_imperatively(entities.IndicatorTypeSettings, tables.indicator_types)

base_kpi_mapper = mapper.map_imperatively(
    entities.FacilityKPI,
    tables.facility_kpi,
    polymorphic_identity='base',
    polymorphic_on=tables.facility_kpi.c.facility_level,
    properties={
        'factory_type': relationship(
            entities.FactoryType, uselist=False, lazy='subquery', viewonly=True
        ),
        'factory': relationship(
            entities.Factory, uselist=False, lazy='subquery', viewonly=True
        ),
        'facility': relationship(
            entities.OrganizationUnit,
            uselist=False,
            lazy='subquery',
            viewonly=True
        )
    }
)
company_kpi_mapper = mapper.map_imperatively(
    entities.CompanyKPI,
    tables.facility_kpi,
    inherits=base_kpi_mapper,
    polymorphic_identity=constants.FacilityLevels.COMPANY,
)
factory_type_kpi_mapper = mapper.map_imperatively(
    entities.FactoryTypeKPI,
    tables.facility_kpi,
    inherits=company_kpi_mapper,
    polymorphic_identity=constants.FacilityLevels.FACTORY_TYPE,
)
factory_kpi_mapper = mapper.map_imperatively(
    entities.FactoryKPI,
    tables.facility_kpi,
    inherits=factory_type_kpi_mapper,
    polymorphic_identity=constants.FacilityLevels.FACTORY,
)
mapper.map_imperatively(
    entities.DepartmentKPI,
    tables.facility_kpi,
    inherits=factory_kpi_mapper,
    polymorphic_identity=constants.FacilityLevels.DEPARTMENT,
)

mapper.map_imperatively(
    division_filler_entities.OrganizationUnit,
    tables.organization_units,
    properties={
        'parent': relationship(
            division_filler_entities.OrganizationUnit,
            uselist=False,
            remote_side=tables.organization_units.c.id,
            lazy='joined',
            join_depth=5,
            viewonly=True
        ),
    }
)

mapper.map_imperatively(
    entities.CheckListOrgUnit,
    tables.organization_units,
    properties={
        'parent': relationship(
            entities.CheckListOrgUnit,
            uselist=False,
            remote_side=tables.organization_units.c.id,
            lazy='joined',
            join_depth=10,
            viewonly=True
        ),
    }
)

mapper.map_imperatively(entities.Facility, tables.organization_units)

mapper.map_imperatively(
    entities.DivisionFacility,
    tables.divisions,
    properties={
        'facility': relationship(
            entities.Facility, uselist=False, lazy='raise', viewonly=True
        ),
        'factory': relationship(
            entities.FactoryFacility,
            uselist=False,
            lazy='raise',
            back_populates='divisions',
            viewonly=True
        )
    }
)

mapper.map_imperatively(
    entities.FactoryFacility,
    tables.factories,
    properties={
        '_name': tables.factories.c.name,
        'factory_type': relationship(
            entities.FactoryTypeFacility,
            uselist=False,
            back_populates='factories',
            lazy='raise',
            viewonly=True
        ),
        'facility': relationship(
            entities.Facility, uselist=False, lazy='raise', viewonly=True
        ),
        'divisions': relationship(
            entities.DivisionFacility,
            uselist=True,
            back_populates='factory',
            lazy='raise',
            viewonly=True
        )
    }
)

mapper.map_imperatively(
    entities.FactoryTypeFacility,
    tables.factory_types,
    properties={
        'factories': relationship(
            entities.FactoryFacility,
            uselist=True,
            back_populates='factory_type',
            lazy='raise',
            viewonly=True
        ),
        '_name': tables.factory_types.c.name
    }
)

mapper.map_imperatively(
    entities.FacilityIndicatorEstimate, tables.indicator_estimates
)

mapper.map_imperatively(
    entities.FacilityIndicatorEstimateDraft, tables.indicator_estimates_draft
)

base_facility_section_estimate_mapper = mapper.map_imperatively(
    entities.FacilitySectionEstimate,
    tables.section_estimates,
    polymorphic_on=tables.section_estimates.c.section,
    polymorphic_abstract=True,
    polymorphic_identity='base'
)

mapper.map_imperatively(
    entities.FacilitySectionEstimateIS,
    tables.section_estimates,
    inherits=base_facility_section_estimate_mapper,
    polymorphic_identity=constants.FacilityEstimateSections.INDUSTRIAL_SAFETY
)

mapper.map_imperatively(
    entities.FacilitySectionEstimateWS,
    tables.section_estimates,
    inherits=base_facility_section_estimate_mapper,
    polymorphic_identity=constants.FacilityEstimateSections.WORK_SAFETY
)

mapper.map_imperatively(
    entities.FacilitySectionEstimateSC,
    tables.section_estimates,
    inherits=base_facility_section_estimate_mapper,
    polymorphic_identity=constants.FacilityEstimateSections.SAFETY_CULTURE
)

mapper.map_imperatively(
    entities.FacilitySectionEstimateTotal,
    tables.section_estimates,
    inherits=base_facility_section_estimate_mapper,
    polymorphic_identity=constants.FacilityEstimateSections.TOTAL
)

mapper.map_imperatively(
    entities.FacilitySectionEstimateDraft,
    tables.section_estimates_draft,
)

mapper.map_imperatively(
    entities.FacilityDriverEstimate, tables.driver_estimates
)

mapper.map_imperatively(
    entities.FactoryFacilityTotalTable,
    tables.factories,
    properties={
        'facility': relationship(
            entities.Facility, uselist=False, lazy='raise', viewonly=True
        ),
        'factory_type': relationship(
            entities.FactoryTypeFacility,
            uselist=False,
            lazy='raise',
            viewonly=True
        ),
        'total_estimates': relationship(
            entities.FacilitySectionEstimate,
            lazy='raise',
            viewonly=True,
            uselist=True
        )
    }
)

mapper.map_imperatively(
    entities.FactoryFacilityTotalTableDraft,
    tables.factories,
    properties={
        'facility': relationship(
            entities.Facility, uselist=False, lazy='raise', viewonly=True
        ),
        'factory_type': relationship(
            entities.FactoryTypeFacility,
            uselist=False,
            lazy='raise',
            viewonly=True
        ),
        'total_estimates': relationship(
            entities.FacilitySectionEstimateDraft,
            lazy='raise',
            viewonly=True,
            uselist=True
        )
    }
)

mapper.map_imperatively(
    route_maintenance_entities.Factory,
    tables.factories,
    properties={
        'unit_id': tables.factories.c.organization_unit_id,
    }
)
mapper.map_imperatively(
    route_maintenance_entities.RouteMaintenance,
    tables.route_maintenance,
    properties={
        '_month': tables.route_maintenance.c.month,
        '_year': tables.route_maintenance.c.year
    }
)

base_irrigation_rating_mapper = mapper.map_imperatively(
    irrigation_rating_entities.IrrigationRating,
    tables.irrigation_rating,
    polymorphic_on=tables.irrigation_rating.c.group,
    polymorphic_abstract=True
)

mapper.map_imperatively(
    irrigation_rating_entities.WinningIrrigationRating,
    inherits=base_irrigation_rating_mapper,
    polymorphic_identity=constants.DepartmentGroups.WINNING
)

mapper.map_imperatively(
    irrigation_rating_entities.TunnelingIrrigationRating,
    inherits=base_irrigation_rating_mapper,
    polymorphic_identity=constants.DepartmentGroups.TUNNELING
)

base_sensors_mapper = mapper.map_imperatively(
    sensors_entities.SensorsCount,
    tables.sensors_control,
    polymorphic_on=tables.sensors_control.c.sensor_type,
    polymorphic_abstract=True
)

mapper.map_imperatively(
    sensors_entities.COSensorsCount,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.CO
)

mapper.map_imperatively(
    sensors_entities.CH4SensorsCount,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.CH4
)

mapper.map_imperatively(
    sensors_entities.TriangleEvents,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.TRIANGLE
)

mapper.map_imperatively(
    sensors_entities.BridgeCount,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.BRIDGE
)

mapper.map_imperatively(
    sensors_entities.EfficiencyAgk,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.EFFICIENCY_AGK
)

mapper.map_imperatively(
    sensors_entities.OxygenContent,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.OXYGEN_CONTENT
)

mapper.map_imperatively(
    sensors_entities.AirTemperature,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.AIR_TEMPERATURE
)

mapper.map_imperatively(
    sensors_entities.COContent,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.CO_CONTENT
)

mapper.map_imperatively(
    sensors_entities.COQuantity,
    inherits=base_sensors_mapper,
    polymorphic_identity=constants.SensorTypes.CO_QUANTITY
)

mapper.map_imperatively(entities.RemoteSource, tables.remote_sources)

base_ais_mapper = mapper.map_imperatively(
    ais_entities.AISVideosStat,
    tables.ais_lights_video_stats,
    polymorphic_on=tables.ais_lights_video_stats.c.ais_type,
    polymorphic_abstract=True
)

mapper.map_imperatively(
    ais_entities.AISVideoStatDC,
    inherits=base_ais_mapper,
    polymorphic_identity=ais_constants.AISTypes.DYNAMIC_CONDITIONS
)

mapper.map_imperatively(
    ais_entities.AISVideoStatAGC,
    inherits=base_ais_mapper,
    polymorphic_identity=ais_constants.AISTypes.AIR_GAS_CONTROL
)

mapper.map_imperatively(ais_entities.AISVideo, tables.ais_lights_videos)


class AISLights:
    mapper.map_imperatively(
        ais_lights_entities.VideoFactories, tables.ais_lights_videos
    )


class Employee:
    mapper.map_imperatively(
        violation_transfer_entities.Employee, tables.employees_hsei
    )


class Violations:
    mapper.map_imperatively(
        violation_transfer_entities.Violation,
        tables.violations,
        properties={
            'inspector': relationship(
                violation_transfer_entities.Employee,
                uselist=False,
            )
        }
    )

    mapper.map_imperatively(
        violation_transfer_entities.ViolationParameter,
        tables.violation_parameters
    )


class Indicators:
    mapper.map_imperatively(
        template_transfer_entities.Indicator, tables.estimate_indicators
    )
    mapper.map_imperatively(entities.CompanyStats, tables.company_stats)


class Organizations:
    mapper.map_imperatively(
        org_transfer_entities.Organization, tables.organization_units
    )


class OperationPlaces:
    mapper.map_imperatively(
        org_transfer_entities.OperationPlace, tables.operation_places
    )
    mapper.map_imperatively(
        template_transfer_entities.Facility, tables.organization_units
    )
    mapper.map_imperatively(
        template_transfer_entities.DivisionFacility,
        tables.divisions,
        properties={
            'facility': relationship(
                template_transfer_entities.Facility,
                uselist=False,
                lazy='raise',
                viewonly=True,
            )
        }
    )

    mapper.map_imperatively(
        template_transfer_entities.FactoryFacility,
        tables.factories,
        properties={
            'facility': relationship(
                template_transfer_entities.Facility,
                uselist=False,
                lazy='raise',
                viewonly=True,
            ),
        }
    )

    mapper.map_imperatively(
        template_transfer_entities.FactoryTypeFacility,
        tables.factory_types,
        properties={'_name': tables.factory_types.c.name}
    )


class Templates:
    mapper.map_imperatively(
        template_transfer_entities.TemplateCriterion,
        tables.template_criteria,
        properties={
            'control_params': relationship(
                template_transfer_entities.CriterionParameter,
                uselist=True,
                lazy='subquery'
            )
        }
    )
    mapper.map_imperatively(
        template_transfer_entities.CriterionParameter,
        tables.template_criteria_control_params
    )
    mapper.map_imperatively(
        template_transfer_entities.ChecklistTemplate,
        tables.check_lists_templates,
        properties={
            'factory_types': relationship(
                template_transfer_entities.FactoryTypeFacility,
                secondary=tables.facility_templates,
            ),
            'factories': relationship(
                template_transfer_entities.FactoryFacility,
                secondary=tables.facility_templates,
            ),
            'divisions': relationship(
                template_transfer_entities.DivisionFacility,
                secondary=tables.facility_templates,
            ),
            'indicator': relationship(
                template_transfer_entities.Indicator,
                uselist=False,
                lazy='subquery'
            ),
            'criteria': relationship(
                template_transfer_entities.TemplateCriterion,
                primaryjoin=(
                    tables.check_lists_templates.c.id ==    # noqa: W504
                    tables.template_criteria.c.template_id
                ),
                uselist=True,
                lazy='subquery'
            )
        }
    )

mapper.map_imperatively(
    entities.Visit,
    tables.visits,
    properties={
        'employee': relationship(
            entities.Employee,
            uselist=False,
            viewonly=True,
            lazy='joined',
        )
    }
)
