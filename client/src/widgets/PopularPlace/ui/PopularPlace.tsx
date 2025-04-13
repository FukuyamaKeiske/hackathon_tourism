import { FC } from "react";
import { Place } from "../model/types";

const PopularPlace: FC<{
    title: string;
    time: string[];
    cost: number;
    badges: string[];
    places: Place[];
}> = ({ title, time, cost, badges, places }) => {
    return (
        <div className="bg-white rounded-lg z-2 shadow-md p-4 mb-[10px] max-w-[calc(100%-5px)]">
            <h2 className="text-xl font-semibold mb-2">{title}</h2>
            <div className="flex gap-40">
                <div className="flex flex-col mb-4">
                    <div className="flex items-center text-gray-500 text-sm">
                        <img src="/mark.png" className="w-5 aspect-square mr-2"/>
                        <span>{time.join(" - ")}</span>
                    </div>
                    <div className="text-[17px]">
                        ~${cost} 
                        <span className="text-gray-500 text-sm">/person</span>
                    </div>
                </div>
                <div className="flex space-x-2 mb-4 relative">
                    {badges.map((badge, index) => (
                        <div
                            key={index}
                            className="relative"
                            style={{
                                marginLeft: index === 0 ? 0 : -25,
                                zIndex: index,
                            }}
                        >
                            <img
                                src={`./${badge}.png`}
                                alt={`badge-${badge}`}
                                className="w-10 aspect-square rounded-full"
                            />
                        </div>
                    ))}
                </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
                {places.map((place, index) => (
                    <div
                        key={index}
                        className="relative rounded-lg overflow-hidden"
                    >
                        <div
                            className="w-full h-32 bg-cover bg-center rounded-lg relative overflow-hidden"
                            style={{ backgroundImage: `url(${place.url})` }}
                        >
                            {place.scores && (
                                <div
                                    className="absolute bottom-0 left-0 bg-[#FF107B] text-white px-3 rounded-tr-lg z-10"
                                    style={{ transform: "translateX(-10px)"}}
                                >
                                    <div className="flex items-center">
                                        <span className="text-xs font-medium">+{place.scores}</span>
                                        <img src="./star.png" className="w-3 aspect-square ml-1"/>
                                    </div>
                                </div>
                            )}
                        </div>
                        <h3 className="text-sm font-semibold mb-1 leading-none mt-2">{place.title}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PopularPlace;