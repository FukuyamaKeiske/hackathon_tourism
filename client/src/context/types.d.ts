import { Map, Marker } from "@2gis/mapgl/types";

export interface MapContextType {
    mapInstance: Map | null
    setMapInstance: React.Dispatch<React.SetStateAction<Map | null>>
    originMarker: Marker | null
    setOriginMarker: React.Dispatch<React.SetStateAction<Marker | null>>
}