import { FC, memo } from "react";

const SearchBar: FC<{ title: string }> = ({ title }) => {
    return (
        <>
            <div className="flex items-center bg-[#F9F9F9] gap-4 pt-[12px] pb-[12px] pr-[16px] pl-[16px] rounded-full max-w-screen">
                <img src="/magnifier.png" className="w-5 h-5"/>
                <a className="font-[Inter] text-xl font-medium">
                    <input type="text" placeholder={title} className="outline-none placeholder:text-[#000000] w-[200px]" />
                </a>
            </div>
        </>
    )
}

export default memo(SearchBar);