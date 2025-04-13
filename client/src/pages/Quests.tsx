import { FC } from "react";
import BottomPanel from "../widgets/BottomPanel/ui/BottomPanel";
import QuestWidget from "../widgets/QuestsWidget/ui/QuestsWidget";
import Header from "../widgets/Header/ui/Header";
import { MapProvider } from "../context/MapContext";

const Profile: FC = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center">
                <Header />
                <MapProvider>
                    <QuestWidget/>
                </MapProvider>
                <BottomPanel activePage="Квесты"/>
            </div>
        </>
    );
};

export default Profile;