// Пример обновленного useMap.ts
import { createContext, useContext, useState } from "react";
import { MapContextType } from "./types";

const MapContext = createContext<MapContextType | undefined>(undefined);

export function MapProvider({ children }: { children: React.ReactNode }) {
  const [mapInstance, setMapInstance] = useState<any>(null);
  const [originMarker, setOriginMarker] = useState<any>(null);
  const [markers, setMarkers] = useState<any[]>([]);

  const value = {
    mapInstance,
    setMapInstance,
    originMarker,
    setOriginMarker,
    markers,
    setMarkers,
  };

  return <MapContext.Provider value={value}>{children}</MapContext.Provider>;
}

export const useMap = () => {
  const context = useContext(MapContext);
  if (context === undefined) {
    throw new Error("useMap must be used within a MapProvider");
  }
  return context;
};