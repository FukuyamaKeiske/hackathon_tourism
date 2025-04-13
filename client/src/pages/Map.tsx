import { FC } from "react";
import Header from "../widgets/Header/ui/Header";
import BottomPanel from "../widgets/BottomPanel/ui/BottomPanel";
import MapWidget from "../widgets/MapWidget/ui/MapWidget";
import {MapProvider} from "../context/MapContext";

const Map: FC = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center">
                <Header />
                <MapProvider>
                    <MapWidget/>
                </MapProvider>
                <BottomPanel activePage="Карта"/>
            </div>
        </>
    );
};

export default Map;