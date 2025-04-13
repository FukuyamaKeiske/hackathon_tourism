import { FC, useEffect, useState } from "react";
import { load } from "@2gis/mapgl";
import { useMap } from "../../../context/MapContext";
import { APIQuest } from "../../../utils/types";
import { getQuests } from "../../../utils/api";

const QuestWidget: FC = () => {
  const mapContext = useMap();
  const [quests, setQuests] = useState<APIQuest[]>([]);
  const [currentQuest, setCurrentQuest] = useState<APIQuest | null>(null);
  let mapModule: any = null;
  let mapInstance: any = null;

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      console.log("Geolocation received:", position.coords);

      load().then((map) => {
        console.log("2GIS map loaded");
        mapModule = map;
        mapInstance = new map.Map("map-container", {
          center: [position.coords.longitude, position.coords.latitude],
          zoom: 13,
          key: "c2259912-6dc2-4517-bc47-670c9e8fd570",
        });

        mapContext.setMapInstance(mapInstance);
        console.log("Map instance set");

        mapContext.setOriginMarker(
          new mapModule.Marker(mapInstance, {
            coordinates: [position.coords.longitude, position.coords.latitude],
          })
        );
        console.log("Origin marker set");

        // Получаем квесты
        getQuests()
          .then((res) => {
            console.log("Quests received:", res);
            setQuests(res);

            // Создаем маркеры для квестов
            const newMarkers = res.map((quest, index) => {
              console.log(
                `Creating marker ${index} at coordinates:`,
                quest.coordinates
              );
              return new mapModule.Marker(mapInstance, {
                coordinates: [quest.coordinates.lng, quest.coordinates.lat],
                // Временно убираем кастомную иконку для теста
                icon: "https://docs.2gis.com/img/mapgl/exclamation-mark.svg",
                size: [100, 100],
              });
            });

            console.log("Markers created:", newMarkers);
            mapContext.setMarkers(newMarkers);

            newMarkers.forEach((marker, index) => {
              marker.on("click", () => {
                console.log("Marker clicked:", res[index]);
                setCurrentQuest(res[index]);
              });
            });
          })
          .catch((error) => {
            console.error("Error fetching quests:", error);
          });
      });
    });

    return () => {
      console.log("Cleaning up map");
      mapContext.mapInstance?.destroy();
      mapContext.setMarkers([]);
    };
  }, []);

  return (
    <div className="bg-[#F9F9F9] w-full h-[calc(100vh-20px)] mt-[10px] m-1 overflow-y-auto flex flex-col items-center">
      <div id="map-container" className="w-full h-full"></div>
      {currentQuest && (
        <div className="absolute bottom-10 bg-white p-4 rounded-lg shadow-lg max-w-md">
          <h3 className="text-lg font-bold">{currentQuest.title}</h3>
          <p>{currentQuest.description}</p>
          <p>Прогресс: {Math.round(currentQuest.progress * 100)}%</p>
          <p>Награда: {currentQuest.reward_points} очков</p>
          {currentQuest.link && (
            <a href={currentQuest.link} className="text-blue-500 underline">
              Подробнее
            </a>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestWidget;