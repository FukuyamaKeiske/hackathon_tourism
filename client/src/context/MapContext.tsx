import { FC, createContext, useMemo, useState } from "react";
import { MapContextType } from "./types";
import { Map, Marker } from "@2gis/mapgl/types";

export const MapContext = createContext<MapContextType | undefined>(undefined)

const MapProvider: FC<{ children: React.ReactNode}> = ({ children }) => {
    const [mapInstance, setMapInstance] = useState<Map | null>(null);
    const [originMarker, setOriginMarker] = useState<Marker | null>(null);
    const values = useMemo(() => ({ mapInstance, setMapInstance, originMarker, setOriginMarker }), [mapInstance, setMapInstance, originMarker, setOriginMarker])

    return (
        <MapContext.Provider value={values}>
            {children}
        </MapContext.Provider>
    );
};

export default MapProvider;