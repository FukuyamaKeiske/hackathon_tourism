import { FC } from "react";
import BottomPanel from "../widgets/BottomPanel/ui/BottomPanel";
import ProfileHeader from "../widgets/ProfileHeader/ui/ProfileHeader";
import Achievements from "../widgets/Achievements/ui/Achievements";
import DigitalSouvenirs from "../widgets/DigitalSouvenirs/ui/DigitalSouvenirs";

const Profile: FC = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center">
                <ProfileHeader />
                <Achievements />
                <DigitalSouvenirs/>
                <BottomPanel activePage="Профиль"/>
            </div>
        </>
    );
};

export default Profile;