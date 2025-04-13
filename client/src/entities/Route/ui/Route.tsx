import { FC, useState } from "react";
import { APIRoute } from "../../../utils/types";

const Route: FC<{ routeData: APIRoute, allRoutes: APIRoute[] }> = ({ routeData, allRoutes }) => {
    const [currentRoute, setCurrentRoute] = useState<APIRoute>(routeData);
    const onClickMore = () => {
        const index = allRoutes.findIndex((route) => route.id === routeData.id);
        if (index + 1 < allRoutes.length) setCurrentRoute(allRoutes[index + 1]);
    }

    return (
        <div className={`${routeData ? '' : 'hidden'} p-4 absolute z-4 flex gap-2 bg-[#F9F9F9] rounded-lg top-[calc(100vh-270px)]`}>
            <div>
                <img src={currentRoute.gallery[0]} className="w-20 aspect-square rounded-lg"/>
            </div>
            <div className="flex flex-col gap-5">
                <span className="font-semibold text-xl overflow-hidden whitespace-nowrap">{currentRoute.name}</span>
                <div className="flex gap-27 items-center">
                    <span className="text-sm font-medium">{currentRoute.work_time}</span>
                    <div className="bg-[#D4EED4] p-2 text-[#76c976] rounded-full" onClick={() => onClickMore()}>
                        Далее
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Route;