export interface IBuildingArtifact {
  [key: string]: string
  artifacts_id: string,
  filename: string,
  file_path: string,
  last_modified: string
}

export interface IBuildingConstructionSection {
  name: string,
  description: string,
  id: string,
  hasSensor: boolean,
  bimArtifacts: IBuildingArtifact[]
}

export interface IBuildingAddress {
  [key: string]: string
  country: string,
  region: string,
  district: string,
  city: string,
  settlement: string,
  street: string,
  building: string,
  room: string,
  note: string
}

export interface IBuildingIndicator {
  [key: string]: string
  name: string,
  value: string,
  measure: string
}

export interface IBuildingExtra {
  objectCategory: {
    title: string,
    text: string
  },
  objectClass: {
    title: string,
    text: string
  },
  objectNote: {
    title: string,
    text: string
  }
}

export interface IBuildingConstructionPart {
  objectId: string,
  name: string,
  address: IBuildingAddress,
  powerIndicators: IBuildingIndicator[],
  technicalIndicators: IBuildingIndicator[],
  energyEfficiency: string,
  fireDangerCategory: string,
  peoplePermanentStay: string,
  responsibilityLevel: string,
  id: string,
  sections: IBuildingConstructionSection[]
}

export interface IBuilding {
  name: string,
  constructionType: number,
  constructionDuration: number,
  address: IBuildingAddress,
  technicalIndicators: IBuildingIndicator[],
  powerIndicators: IBuildingIndicator[],
  extra: IBuildingExtra,
  id: string,
  constructionParts: IBuildingConstructionPart[],
  documentArtifacts: IBuildingArtifact[]
}

export interface IBuildingSectionSensors {
  sensor_id: string,
  sensor_address: string,
  sensor_name: string,
  sensor_description: string,
  sensor_unit: string,
  monitoring_name: string,
  monitoring_location: string,
  connection_name: string,
  construction_section_id: string
}

export interface IBuildingSectionSensorData {
  time: string,
  value: number,
  monitoring_name: string,
  monitoring_location: string,
  connection_name: string,
  sensor_address: string,
  sensor_name: string,
  sensor_unit: string,
  sensor_description: string
}
