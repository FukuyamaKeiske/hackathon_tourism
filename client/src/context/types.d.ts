import { Map, Marker } from "@2gis/mapgl/types";

export interface MapContextType {
    mapInstance: any; // Замените на более конкретный тип, если доступен
    setMapInstance: (instance: any) => void;
    originMarker: any; // Тип маркера
    setOriginMarker: (marker: any) => void;
    markers: any[]; // Массив маркеров
    setMarkers: (markers: any[]) => void;
}