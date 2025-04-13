import { FC } from 'react';
import BottomPanelButton from '../../../shared/BottomPanelButton/ui/BottomPanelButton';

const buttons = [
    {
        title: 'Карта',
        imagePath: 'magnifier',
        path: '/'
    },
    {
        title: 'Награды',
        imagePath: 'diamond',
        path: '/rewards',
    },
    {
        title: 'Квесты',
        imagePath: 'grey_star',
        path: '/quests',
    },
    {
        title: 'Брони',
        imagePath: 'money',
        path: '/bookings',
    },
    {
        title: 'Профиль',
        imagePath: 'persons',
        path: '/profile',
    },
]

const BottomPanel: FC<{ activePage: string }> = ({ activePage }) => {
    return (
        <nav className="bg-white fixed shadow-xl bottom-0 z-50 rounded-t-[35px] left-0 right-0 flex justify-around items-center p-2 min-h-30">
            {buttons.map((button, index) => (
                <BottomPanelButton key={index} title={button.title} imagePath={button.imagePath} path={button.path} isActive={activePage == button.title}/>
            ))}
        </nav>
    );
};

export default BottomPanel;