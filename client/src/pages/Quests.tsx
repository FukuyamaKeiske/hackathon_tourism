import { FC } from "react";
import BottomPanel from "../widgets/BottomPanel/ui/BottomPanel";

const Profile: FC = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center">
                <BottomPanel activePage="Квесты"/>
            </div>
        </>
    );
};

export default Profile;