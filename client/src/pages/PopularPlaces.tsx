import { FC } from "react";
import Header from "../widgets/Header/ui/Header";
import PopularPlacesWidget from "../widgets/PopularPlacesWidget/ui/PopularPlacesWidget";
import BottomPanel from "../widgets/BottomPanel/ui/BottomPanel";

const PopularPlaces: FC = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center">
                <Header />
                <PopularPlacesWidget />
                <BottomPanel />
                <div className="absolute bottom-0 z-3 w-full h-[30vh] bg-gradient-to-t from-gray-400 to-transparent pointer-events-none"></div>
            </div>
        </>
    );
};

export default PopularPlaces;