import { FC, useEffect, useState } from "react";
import { load } from "@2gis/mapgl";
import { Ruler } from "@2gis/mapgl-ruler";
import { useMap } from "../../../hooks/useMap";
import LocationContextMenu from "../../../shared/LocationContextMenu/ui/LocationContextMenu";
import Route from "../../../entities/Route/ui/Route";
import { APIRoute } from "../../../utils/types";
import { getRoute } from "../../../utils/api";

const MapWidget: FC = () => {
    const mapContext = useMap();
    const [allRoutes, setRoutes] = useState<APIRoute[]>([]);
    let rulerInstance: null | Ruler = null; 
    const [currentPlace, setCurrentPlace] = useState<APIRoute | null>(null);

    useEffect(() => {
        navigator.geolocation.getCurrentPosition((position) => {
            load().then((map) => {
                const mapInstance = new map.Map("map-container", {
                    center: [position.coords.longitude, position.coords.latitude],
                    zoom: 13,
                    key: "c2259912-6dc2-4517-bc47-670c9e8fd570",
                });

                const routes = getRoute(position.coords.latitude.toString(), position.coords.longitude.toString())
                routes.then(res => setRoutes(res))
                mapContext.setMapInstance(mapInstance);

                allRoutes.forEach((route) => {
                    const marker = new map.Marker(mapInstance, {
                        coordinates: [route.coordinates.lng, route.coordinates.lat],
                        icon: route.partner ? 'https://docs.2gis.com/img/mapgl/marker.svg' : '',
                        size: route.partner ? [40, 40] : [20, 20],
                        
                    });

                    marker.on("click", () => {
                        console.log(route)
                        setCurrentPlace(route)
                    });
                });

                mapContext.setOriginMarker(
                    new map.Marker(mapInstance, {
                        coordinates: [position.coords.longitude, position.coords.latitude],
                    })
                );
            });
        });

        return () => {
            if (rulerInstance) {
                rulerInstance.destroy();
            }
            mapContext.mapInstance?.destroy(); 
        };
    }, []);

    const handleYesClick = () => {
        if (!mapContext.mapInstance) return;

        const routeCoordinates = allRoutes.map((route) => [route.coordinates.lng, route.coordinates.lat]);

        if (rulerInstance) {
            rulerInstance.destroy();
            rulerInstance = null;
        }

        rulerInstance = new Ruler(mapContext.mapInstance, {
            mode: "polyline",
            points: routeCoordinates,
        });
    };

    // Колбэк для кнопки "Нет"
    const handleNoClick = () => {
        if (rulerInstance) {
            rulerInstance.destroy();
            rulerInstance = null;
        }
    };

    return (
        <div className="bg-[#F9F9F9] w-full h-[calc(100vh-20px)] mt-[10px] m-1 overflow-y-auto flex flex-col items-center">
            <div id="map-container" className="w-full h-full"></div>
            <LocationContextMenu
                title="Вы находитесь здесь?"
                variants={["Да", "Нет"]}
                onClickFirst={handleYesClick}
                onClickSecond={handleNoClick} 
            />
            {currentPlace && <Route routeData={currentPlace} allRoutes={allRoutes} />}
        </div>
    );
};

export default MapWidget;