import { FC } from "react";
import PopularPlace from "../../PopularPlace/ui/PopularPlace";

// Пример данных для мест
const popularPlacesData = [
    {
        title: "Активный отдых",
        time: ["9:00", "10:00"],
        cost: 169,
        badges: ["blue_tag", "green_tag", "orange_tag"],
        places: [
            {
                title: "Берендеево царство",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
            },
            {
                title: "Веревочный парк \"Sky Park\"",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
                scores: 300,
            },
            {
                title: "Пляж",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
            },
        ],
    },
    {
        title: "Культурный отдых",
        time: ["14:00", "16:00"],
        cost: 250,
        badges: ["blue_tag", "green_tag", "orange_tag"],
        places: [
            {
                title: "Музей изобразительных искусств",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
            },
            {
                title: "Театр оперы и балета",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
                scores: 500,
            },
        ],
    },
    {
        title: "Культурный отдых",
        time: ["14:00", "16:00"],
        cost: 250,
        badges: ["blue_tag", "green_tag", "orange_tag"],
        places: [
            {
                title: "Музей изобразительных искусств",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
            },
            {
                title: "Театр оперы и балета",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
                scores: 500,
            },
        ],
    },
    {
        title: "Культурный отдых",
        time: ["14:00", "16:00"],
        cost: 250,
        badges: ["blue_tag", "green_tag", "orange_tag"],
        places: [
            {
                title: "Музей изобразительных искусств",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
            },
            {
                title: "Театр оперы и балета",
                url: "https://media.istockphoto.com/id/1317323736/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B2%D0%B8%D0%B4-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B1%D0%BE-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2.jpg?s=612x612&w=0&k=20&c=93KAEcJLi6BDbDLjRCZOFhC-XPfCY0BqqMvu1WzywPo=",
                scores: 500,
            },
        ],
    }
];

const PopularPlacesWidget: FC = () => {
    return (
        <div className="bg-[#F9F9F9] w-full h-[calc(100vh-20px)] mt-[10px] m-1 overflow-y-auto flex flex-col items-center">
            {popularPlacesData.map((place, index) => (
                <PopularPlace
                    key={index}
                    title={place.title}
                    time={place.time}
                    cost={place.cost}
                    badges={place.badges}
                    places={place.places}
                />
            ))}
        </div>
    );
};

export default PopularPlacesWidget;