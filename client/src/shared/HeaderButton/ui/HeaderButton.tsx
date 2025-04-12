import { FC, memo } from "react";

const HeaderButton: FC<{ title?: string, imagePath: string, newThings?: number }> = ({ title, imagePath, newThings }) => {
    return (
        <>
            <div className={`flex relative items-center bg-[#F9F9F9] gap-4 pt-[12px] pb-[12px] pl-[14px] ${title ? 'pr-[16px]' : ''} rounded-full`}>
                <img src={`/${imagePath}`} className="w-5 h-5"/>
                <a className="font-[Inter] text-lg font-semibold">
                    {title}
                </a>
                {newThings && 
                    <div className="bg-[#FF107B] absolute w-10 h-7 rounded-full left-1/2 transform translate-y-1/2 text-white flex items-center justify-center">
                        <div className="leading-[-10px] font-medium">
                            +{newThings}
                        </div>
                    </div>
                }
            </div>
        </>
    )
}

export default memo(HeaderButton);