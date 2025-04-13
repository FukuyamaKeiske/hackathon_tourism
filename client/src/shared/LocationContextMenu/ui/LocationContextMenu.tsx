import { FC, useState } from "react"

const LocationContextMenu: FC<{ title: string, variants: string[], onClickFirst: () => void, onClickSecond: () => void }> = ({ title, variants, onClickFirst, onClickSecond }) => {
    const [show, setShow] = useState(false);
    
    return (
        <>
            <div className={`bg-white p-5 rounded-lg w-11/12 flex items-center flex-col absolute z-5 top-[calc(100vh-270px)] gap-5 ${show ? 'hidden' : ''}`}>
                <div>
                    <span className="font-semibold text-xl">{title}</span>
                </div>
                <div className="flex gap-2">
                    {variants.map((variant, index) => (
                        <div key={index} className="cursor-pointer bg-[#F9F9F9] rounded-full py-3 px-15 text-[#505050] text-md" onClick={() => {
                            index === 0 ? onClickFirst() : onClickSecond()
                            setShow(true)
                        }}>{variant}</div>
                    ))}
                </div>
            </div>
        </>
    )
}

export default LocationContextMenu;
