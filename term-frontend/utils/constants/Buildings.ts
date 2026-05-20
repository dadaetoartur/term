import type {
  IBuilding, IBuildingAddress, IBuildingArtifact, IBuildingConstructionPart, IBuildingConstructionSection,
  IBuildingExtra, IBuildingIndicator, IBuildingSectionSensorData, IBuildingSectionSensors,
} from '../types/Building';

export const EMPTY_SENSOR_DATA: IBuildingSectionSensorData = {
  time: new Date().toISOString(),
  value: 0,
  monitoring_name: '',
  monitoring_location: '',
  connection_name: '',
  sensor_address: '',
  sensor_name: '',
  sensor_unit: '',
  sensor_description: '',
};

export const EMPTY_SENSOR: IBuildingSectionSensors = {
  sensor_id: '',
  sensor_address: '',
  sensor_name: '',
  sensor_description: '',
  sensor_unit: '',
  monitoring_name: '',
  monitoring_location: '',
  connection_name: '',
  construction_section_id: '',
};

export const EMPTY_INDICATOR: IBuildingIndicator = {
  name: '',
  value: '',
  measure: '',
};

export const EMPTY_ARTIFACT: IBuildingArtifact = {
  artifacts_id: '',
  filename: '',
  file_path: '',
  last_modified: '',
};

export const EMPTY_EXTRA: IBuildingExtra = {
  objectCategory: {
    title: '',
    text: '',
  },
  objectClass: {
    title: '',
    text: '',
  },
  objectNote: {
    title: '',
    text: '',
  },
};

export const EMPTY_ADDRESS: IBuildingAddress = {
  country: '',
  region: '',
  district: '',
  city: '',
  settlement: '',
  street: '',
  building: '',
  room: '',
  note: '',
};

export const EMPTY_CONSTRUCTION_SECTION: IBuildingConstructionSection = {
  name: '',
  description: '',
  id: '',
  hasSensor: false,
  bimArtifacts: [],
};

export const EMPTY_CONSTRUCTION_PART: IBuildingConstructionPart = {
  objectId: '',
  name: '',
  address: { ...EMPTY_ADDRESS },
  powerIndicators: [{ ...EMPTY_INDICATOR }],
  technicalIndicators: [{ ...EMPTY_INDICATOR }],
  energyEfficiency: '',
  fireDangerCategory: '',
  peoplePermanentStay: '',
  responsibilityLevel: '',
  id: '',
  sections: [],
};

export const EMPTY_BUILDING: IBuilding = {
  name: '',
  constructionType: 0,
  constructionDuration: 0,
  address: { ...EMPTY_ADDRESS },
  technicalIndicators: [{ ...EMPTY_INDICATOR }],
  powerIndicators: [{ ...EMPTY_INDICATOR }],
  extra: { ...EMPTY_EXTRA },
  id: '',
  constructionParts: [{ ...EMPTY_CONSTRUCTION_PART }],
  documentArtifacts: [],
};
