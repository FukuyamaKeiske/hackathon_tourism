import { FC } from "react"
import { useNavigate } from "react-router"

const BottomPanelButton: FC<{ title: string, imagePath: string, path: string, isActive?: boolean }> = ({ title, imagePath, path, isActive }) => {
    const navigate = useNavigate()

    return (
        <>
            <div className="flex flex-col items-center justify-center" onClick={() => navigate(path)}>
                <div className={`${isActive ? 'bg-[#FF107B]' : 'bg-[#F9F9F9]'} w-12 h-12 rounded-full flex items-center justify-center mb-2}`}>
                    <img src={`./${imagePath}.png`} className="w-6 h-6"/>
                </div>
                <div className="text-sm font-medium text-[#868686]">
                    {title}
                </div>
            </div>
        </>
    )
}

export default BottomPanelButton