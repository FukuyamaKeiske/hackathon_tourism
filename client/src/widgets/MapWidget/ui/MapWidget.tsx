import { FC, useEffect, useState } from "react";
import { load } from "@2gis/mapgl";
import { Ruler } from "@2gis/mapgl-ruler";
import LocationContextMenu from "../../../shared/LocationContextMenu/ui/LocationContextMenu";
import Route from "../../../entities/Route/ui/Route";
import { APIRoute } from "../../../utils/types";
import { getRoute } from "../../../utils/api";
import { useMap } from "../../../context/MapContext";
import { useNavigate } from "react-router";

const MapWidget: FC = () => {
  const mapContext = useMap();
  const [allRoutes, setRoutes] = useState<APIRoute[]>([]);
  let rulerInstance: null | Ruler = null;
  const [currentPlace, setCurrentPlace] = useState<APIRoute | null>(null);
  let mapModule: any = null;
  let mapInstance: any = null;
  const navigate = useNavigate();

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      load().then((map) => {
        mapModule = map;
        mapInstance = new map.Map("map-container", {
          center: [position.coords.longitude, position.coords.latitude],
          zoom: 13,
          key: "c2259912-6dc2-4517-bc47-670c9e8fd570",
        });

        mapContext.setMapInstance(mapInstance);

        mapContext.setOriginMarker(
          new mapModule.Marker(mapInstance, {
            coordinates: [position.coords.longitude, position.coords.latitude],
          })
        );

        getRoute(position.coords.latitude.toString(), position.coords.longitude.toString()).then((res) => {
          const routes = res.route.slice(0, 10);
          setRoutes(routes);

          const newMarkers = routes.map((route) => {
            return new mapModule.Marker(mapInstance, {
              coordinates: [route.coordinates.lng, route.coordinates.lat],
              icon: route.partner ? "https://docs.2gis.com/img/mapgl/marker.svg" : "",
              size: route.partner ? [40, 40] : [20, 20],
            });
          });

          mapContext.setMarkers(newMarkers);

          newMarkers.forEach((marker, index) => {
            marker.on("click", () => {
              setCurrentPlace(routes[index]);
            });
          });
        });
      });
    });

    return () => {
      if (rulerInstance) {
        rulerInstance.destroy();
      }
      mapContext.mapInstance?.destroy();
      mapContext.setMarkers([]);
    };
  }, []);

  const handleYesClick = () => {
    if (rulerInstance) {
      rulerInstance.destroy();
      rulerInstance = null;
    }

    const routeCoordinates = allRoutes.map((route) => [route.coordinates.lng, route.coordinates.lat]);

    rulerInstance = new Ruler(mapContext.mapInstance, {
      mode: "polyline",
      points: routeCoordinates,
    });
  };

  const handleNoClick = () => {
    if (rulerInstance) {
      rulerInstance.destroy();
      rulerInstance = null;
    }
  };

  const handleStartClick = () => {
    if (allRoutes.length > 0) {
      navigate(`/route-details/${allRoutes[0].id}`);
    }
  };

  return (
    <div className="bg-[#F9F9F9] w-full h-[calc(100vh-20px)] mt-[10px] m-1 overflow-y-auto flex flex-col items-center relative">
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