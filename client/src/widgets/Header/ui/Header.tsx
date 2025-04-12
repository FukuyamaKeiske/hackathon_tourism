import { FC } from "react";
import SearchBar from "../../../shared/SearchBar/ui/SearchBar";
import HeaderButton from "../../../shared/HeaderButton/ui/HeaderButton";

const Header: FC = () => {
    return (
        <>
            <div className="mt-[20px] w-full flex flex-col justify-center">
                <div className="m-1">
                    <SearchBar title="Сочи, Россия"/>
                    <div className="flex gap-4 mt-[10px] flex-wrap">
                        <HeaderButton title="2 persons" imagePath="persons.png"/>
                        <HeaderButton title="3 фев, пн" imagePath="calendar.png"/>
                        <HeaderButton imagePath="settings.png" newThings={7}/>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Header;