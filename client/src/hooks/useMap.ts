import { useContext } from 'react';
import { MapContext } from '../context/MapContext';

export const useMap = () => {
    const context = useContext(MapContext);
    if (!context)
        throw new Error('MapContext must be used within an MapProvider');
    return context;
}